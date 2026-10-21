import { Hono } from 'hono';
import { cors } from 'hono/cors';
import {
  evaluateEligibility,
  evaluateAllExams,
  AUTHORITATIVE_EXAM_RULES,
  type UserProfileInput,
  type EligibilityVerdict,
} from './eligibilityEngine';

// Bundled static fallbacks
import rawExams from './data/grade_a_exams.json';
import rawTaxonomy from './data/syllabus_taxonomy.json';
import rawMatrix from './data/exam_syllabus_matrix.json';

export interface Env {
  DB?: D1Database;
  ENVIRONMENT?: string;
  API_VERSION?: string;
}

const app = new Hono<{ Bindings: Env }>();

// Enable CORS for all incoming cross-origin requests from Vue PWA client
app.use(
  '*',
  cors({
    origin: '*',
    allowMethods: ['GET', 'POST', 'OPTIONS'],
    allowHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
    exposeHeaders: ['Content-Length', 'X-Kuma-Revision'],
    maxAge: 86400,
  })
);

// Fallback data cached in memory
const STATIC_EXAMS: any[] = (rawExams as any).exams || rawExams;
const STATIC_TAXONOMY_TOPICS: any[] = (rawTaxonomy as any).topics_flat || [];
const STATIC_TAXONOMY_LOOKUP: Record<string, any> = (rawTaxonomy as any).lookup_by_id || {};
const STATIC_TAXONOMY_DOMAINS: any[] = (rawTaxonomy as any).domains || [];
const STATIC_MATRIX: any = rawMatrix;

// Root / Health check
app.get('/', (c) => {
  return c.json({
    name: 'Indian Grade A Government Examinations Intelligence Platform API',
    version: '1.0.0',
    status: 'HEALTHY',
    timestamp: new Date().toISOString(),
    endpoints: {
      exams: '/api/v1/exams',
      exam_by_id: '/api/v1/exams/:id',
      syllabus_taxonomy: '/api/v1/syllabus/taxonomy',
      syllabus_matrix: '/api/v1/syllabus/matrix',
      profile_evaluate: '/api/v1/profile/evaluate',
      profile_sync: '/api/v1/profile/sync',
    },
  });
});

app.get('/health', (c) => c.json({ status: 'ok', timestamp: new Date().toISOString() }));
app.get('/api/v1/health', (c) => c.json({ status: 'ok', timestamp: new Date().toISOString() }));

// 1. GET /api/v1/exams
// Returns all 36 Grade A exams with count and success flag
app.get('/api/v1/exams', async (c) => {
  const categoryFilter = c.req.query('category');
  const clusterFilter = c.req.query('cluster');

  // Try D1 if bound
  if (c.env?.DB) {
    try {
      let query = 'SELECT * FROM exams';
      const params: any[] = [];
      if (categoryFilter) {
        query += ' WHERE category = ?';
        params.push(categoryFilter);
      }
      query += ' ORDER BY exam_id ASC';

      const examStmt = params.length > 0 ? c.env.DB.prepare(query).bind(...params) : c.env.DB.prepare(query);
      const examRows = await examStmt.all();

      if (examRows.results && examRows.results.length > 0) {
        // Fetch eligibility criteria to assemble complete records
        const eligRows = await c.env.DB.prepare('SELECT * FROM eligibility_criteria').all();
        const eligMap = new Map((eligRows.results || []).map((row: any) => [row.exam_id, row]));

        const combined = examRows.results.map((e: any) => {
          let timeline = e.tentative_timeline_2027;
          if (typeof timeline === 'string') {
            try {
              timeline = JSON.parse(timeline);
            } catch {}
          }
          const elig: any = eligMap.get(e.exam_id);
          let parsedElig: any = undefined;
          if (elig) {
            parsedElig = {
              ...elig,
              relaxations: typeof elig.relaxations_json === 'string' ? JSON.parse(elig.relaxations_json) : elig.relaxations_json,
              accepted_disciplines: typeof elig.accepted_disciplines === 'string' ? JSON.parse(elig.accepted_disciplines) : elig.accepted_disciplines,
              domicile_restrictions: typeof elig.domicile_restrictions === 'string' ? JSON.parse(elig.domicile_restrictions) : elig.domicile_restrictions,
              language_requirements: typeof elig.language_requirements === 'string' ? JSON.parse(elig.language_requirements) : elig.language_requirements,
              physical_standards: typeof elig.physical_standards === 'string' ? JSON.parse(elig.physical_standards) : elig.physical_standards,
            };
          }
          return {
            ...e,
            tentative_timeline_2027: timeline,
            eligibility: parsedElig,
          };
        });

        return c.json({
          success: true,
          count: combined.length,
          data: combined,
          exams: combined,
          source: 'd1',
        });
      }
    } catch (dbErr) {
      console.warn('D1 query failed in /api/v1/exams, falling back to static catalog:', dbErr);
    }
  }

  // Fallback to static catalog
  let list = STATIC_EXAMS;
  if (categoryFilter) {
    list = list.filter((e) => e.category === categoryFilter);
  }
  if (clusterFilter) {
    list = list.filter((e) => e.cluster === clusterFilter);
  }

  return c.json({
    success: true,
    count: list.length,
    data: list,
    exams: list,
    source: 'bundled',
  });
});

// 2. GET /api/v1/exams/:id
// Returns detailed profile for an exam or 404
app.get('/api/v1/exams/:id', async (c) => {
  const id = c.req.param('id').trim();
  const upperId = id.toUpperCase();

  // Try D1 if bound
  if (c.env?.DB) {
    try {
      const examRow = await c.env.DB.prepare(
        'SELECT * FROM exams WHERE UPPER(exam_id) = ? OR UPPER(short_code) = ?'
      )
        .bind(upperId, upperId)
        .first();

      if (examRow) {
        const eligRow = await c.env.DB.prepare(
          'SELECT * FROM eligibility_criteria WHERE exam_id = ?'
        )
          .bind((examRow as any).exam_id)
          .first();

        let timeline = (examRow as any).tentative_timeline_2027;
        if (typeof timeline === 'string') {
          try {
            timeline = JSON.parse(timeline);
          } catch {}
        }

        let parsedElig: any = undefined;
        if (eligRow) {
          const el: any = eligRow;
          parsedElig = {
            ...el,
            relaxations: typeof el.relaxations_json === 'string' ? JSON.parse(el.relaxations_json) : el.relaxations_json,
            accepted_disciplines: typeof el.accepted_disciplines === 'string' ? JSON.parse(el.accepted_disciplines) : el.accepted_disciplines,
            domicile_restrictions: typeof el.domicile_restrictions === 'string' ? JSON.parse(el.domicile_restrictions) : el.domicile_restrictions,
            language_requirements: typeof el.language_requirements === 'string' ? JSON.parse(el.language_requirements) : el.language_requirements,
            physical_standards: typeof el.physical_standards === 'string' ? JSON.parse(el.physical_standards) : el.physical_standards,
          };
        }

        const fullExam = {
          ...(examRow as any),
          tentative_timeline_2027: timeline,
          eligibility: parsedElig,
        };

        return c.json({
          success: true,
          data: fullExam,
          source: 'd1',
        });
      }
    } catch (dbErr) {
      console.warn(`D1 lookup for exam ${id} failed:`, dbErr);
    }
  }

  // Lookup in static catalog
  const found = STATIC_EXAMS.find(
    (e) =>
      (e.exam_id && e.exam_id.toUpperCase() === upperId) ||
      (e.short_code && e.short_code.toUpperCase() === upperId)
  );

  if (!found) {
    return c.json(
      {
        success: false,
        error: 'Exam not found',
        message: `Exam with ID '${id}' not found`,
      },
      404
    );
  }

  return c.json({
    success: true,
    data: found,
    source: 'bundled',
  });
});

// 3. GET /api/v1/syllabus/taxonomy
// Returns 192 normalized topics
app.get('/api/v1/syllabus/taxonomy', (c) => {
  const domainFilter = c.req.query('domain');
  const subDomainFilter = c.req.query('sub_domain');

  let topics = STATIC_TAXONOMY_TOPICS;
  if (domainFilter) {
    topics = topics.filter((t) => t.domain.toLowerCase() === domainFilter.toLowerCase());
  }
  if (subDomainFilter) {
    topics = topics.filter((t) => t.sub_domain.toLowerCase() === subDomainFilter.toLowerCase());
  }

  return c.json({
    success: true,
    count: topics.length,
    data: topics,
    topics_flat: topics,
    lookup_by_id: STATIC_TAXONOMY_LOOKUP,
    domains: STATIC_TAXONOMY_DOMAINS,
  });
});

// 4. GET /api/v1/syllabus/matrix
// Returns pairwise matrix, overlap metrics, and UpSet combinations
app.get('/api/v1/syllabus/matrix', (c) => {
  const source = c.req.query('source');
  const target = c.req.query('target');

  if (source && target && STATIC_MATRIX.pairwise_metrics) {
    const srcPairs = STATIC_MATRIX.pairwise_metrics[source];
    if (srcPairs && srcPairs[target]) {
      return c.json({
        success: true,
        data: srcPairs[target],
        pair: srcPairs[target],
      });
    }
  }

  return c.json({
    success: true,
    count: Object.keys(STATIC_MATRIX.pairwise_metrics || {}).length,
    metadata: STATIC_MATRIX.metadata,
    exam_summaries: STATIC_MATRIX.exam_summaries,
    pairwise_metrics: STATIC_MATRIX.pairwise_metrics,
    disjoint_upset_combinations: STATIC_MATRIX.disjoint_upset_combinations,
    topic_frequencies: STATIC_MATRIX.topic_frequencies,
    data: STATIC_MATRIX,
  });
});

// 5. POST /api/v1/profile/evaluate
// Evaluates candidate profile using eligibility engine
app.post('/api/v1/profile/evaluate', async (c) => {
  let body: any;
  try {
    body = await c.req.json();
  } catch (err) {
    return c.json(
      {
        success: false,
        error: 'Malformed JSON',
        message: 'Malformed JSON in request body. Expected a valid JSON object.',
      },
      400
    );
  }

  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return c.json(
      {
        success: false,
        error: 'Invalid Request',
        message: 'Request body must be a JSON object containing profile attributes.',
      },
      400
    );
  }

  const profileInput: UserProfileInput = body.profile ? body.profile : body;
  const targetExamId: string | undefined = body.exam_id || c.req.query('exam_id');

  // Single exam evaluation
  if (targetExamId) {
    const rule = AUTHORITATIVE_EXAM_RULES[targetExamId];
    if (!rule) {
      return c.json(
        {
          success: false,
          error: 'Exam Not Found',
          message: `Cannot evaluate eligibility: exam '${targetExamId}' does not exist.`,
        },
        404
      );
    }
    const verdict = evaluateEligibility(profileInput, rule, 2027);
    return c.json({
      success: true,
      status: verdict.status,
      reasons: verdict.reasons,
      relaxations_applied: verdict.relaxations_applied,
      statutory_citation: verdict.statutory_citation,
      verdict,
    });
  }

  // Batch evaluation across all 36 examinations
  const allVerdicts = evaluateAllExams(profileInput, AUTHORITATIVE_EXAM_RULES, 2027);
  const eligible = Object.values(allVerdicts)
    .filter((v) => v.status === 'ELIGIBLE')
    .map((v) => v.exam_id);
  const conditional = Object.values(allVerdicts)
    .filter((v) => v.status === 'CONDITIONALLY_ELIGIBLE')
    .map((v) => v.exam_id);
  const ineligible = Object.values(allVerdicts)
    .filter((v) => v.status === 'INELIGIBLE')
    .map((v) => v.exam_id);

  // If a default verdict for UPSC_CSE is useful for quick checks:
  const defaultVerdict = allVerdicts['UPSC_CSE'];

  return c.json({
    success: true,
    status: defaultVerdict ? defaultVerdict.status : 'EVALUATED',
    reasons: defaultVerdict ? defaultVerdict.reasons : [],
    relaxations_applied: defaultVerdict ? defaultVerdict.relaxations_applied : [],
    statutory_citation: defaultVerdict ? defaultVerdict.statutory_citation : '',
    summary: {
      total_evaluated: Object.keys(allVerdicts).length,
      eligible_count: eligible.length,
      conditionally_eligible_count: conditional.length,
      ineligible_count: ineligible.length,
      eligible_exams: eligible,
      conditionally_eligible_exams: conditional,
      ineligible_exams: ineligible,
    },
    verdicts: allVerdicts,
    data: allVerdicts,
  });
});

// 6. POST /api/v1/profile/sync
// Upserts candidate profile into Cloudflare D1 `user_profiles` table
app.post('/api/v1/profile/sync', async (c) => {
  let body: any;
  try {
    body = await c.req.json();
  } catch (err) {
    return c.json(
      {
        success: false,
        error: 'Malformed JSON',
        message: 'Malformed JSON in request body.',
      },
      400
    );
  }

  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return c.json(
      {
        success: false,
        error: 'Invalid Request',
        message: 'Request body must be a valid JSON object.',
      },
      400
    );
  }

  const userId = (body.user_id || body.userId || '').toString().trim();
  const dob = (body.dob || '').toString().trim();
  const genderRaw = (body.gender || '').toString().trim().toUpperCase();
  const categoryRaw = (body.category || '').toString().trim().toUpperCase();
  const degree = (body.graduation_degree || body.degree || '').toString().trim();
  const discipline = (body.graduation_discipline || body.discipline || '').toString().trim();
  const aggregatePctRaw = body.graduation_aggregate_pct ?? body.aggregate_pct;
  const stateDomicile = (body.state_domicile || body.domicile_state || '').toString().trim();
  const isFinalYear = body.is_final_year ? 1 : 0;
  const name = body.name ? body.name.toString().trim() : null;
  const motherTongue =
    body.mother_tongue || (Array.isArray(body.fluent_languages) ? body.fluent_languages[0] : null) || null;
  const heightCm = body.height_cm != null ? Number(body.height_cm) : null;
  const chestCm = body.chest_cm != null ? Number(body.chest_cm) : null;
  const visionSpecs = body.vision_specs ? JSON.stringify(body.vision_specs) : null;

  // Validation of mandatory fields
  const missingFields: string[] = [];
  if (!userId) missingFields.push('user_id');
  if (!dob) missingFields.push('dob');
  if (!genderRaw) missingFields.push('gender');
  if (!categoryRaw) missingFields.push('category');
  if (!degree) missingFields.push('graduation_degree');
  if (!discipline) missingFields.push('graduation_discipline');
  if (aggregatePctRaw === undefined || aggregatePctRaw === null || isNaN(Number(aggregatePctRaw))) {
    missingFields.push('graduation_aggregate_pct');
  }
  if (!stateDomicile) missingFields.push('state_domicile');

  if (missingFields.length > 0) {
    return c.json(
      {
        success: false,
        error: 'Missing Required Fields',
        message: `Missing mandatory user profile fields: ${missingFields.join(', ')}`,
        missing_fields: missingFields,
      },
      400
    );
  }

  // Validate prior attempts JSON if present
  let priorAttemptsJson: string | null = null;
  if (body.prior_attempts_json != null) {
    if (typeof body.prior_attempts_json === 'string') {
      try {
        JSON.parse(body.prior_attempts_json);
        priorAttemptsJson = body.prior_attempts_json;
      } catch {
        return c.json(
          {
            success: false,
            error: 'Validation Error',
            message: 'prior_attempts_json must be valid JSON.',
          },
          400
        );
      }
    } else {
      priorAttemptsJson = JSON.stringify(body.prior_attempts_json);
    }
  } else if (body.prior_attempts != null) {
    priorAttemptsJson = JSON.stringify(body.prior_attempts);
  }

  // Normalization for gender enum: MALE, FEMALE, OTHER
  const validGenders = ['MALE', 'FEMALE', 'OTHER'];
  const gender = validGenders.includes(genderRaw) ? genderRaw : 'OTHER';

  // Normalization for category enum: GEN, OBC_NCL, SC, ST, EWS, PwBD
  const validCategories = ['GEN', 'OBC_NCL', 'SC', 'ST', 'EWS', 'PWBD'];
  let category = categoryRaw;
  if (category === 'OBC') category = 'OBC_NCL';
  if (category.startsWith('PWBD')) category = 'PwBD';
  if (!validCategories.map((c) => c.toUpperCase()).includes(category.toUpperCase())) {
    category = 'GEN';
  }

  const aggregatePct = Number(aggregatePctRaw);
  if (aggregatePct < 0 || aggregatePct > 100) {
    return c.json(
      {
        success: false,
        error: 'Validation Error',
        message: 'graduation_aggregate_pct must be between 0 and 100.',
      },
      400
    );
  }

  // Persist to D1 if binding is available
  let persisted = false;
  if (c.env?.DB) {
    try {
      await c.env.DB.prepare(`
        INSERT OR REPLACE INTO user_profiles (
          user_id, name, dob, gender, category,
          graduation_degree, graduation_discipline, graduation_aggregate_pct,
          is_final_year, state_domicile, mother_tongue,
          height_cm, chest_cm, vision_specs, prior_attempts_json,
          updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
      `)
        .bind(
          userId,
          name,
          dob,
          gender,
          category,
          degree,
          discipline,
          aggregatePct,
          isFinalYear,
          stateDomicile,
          motherTongue,
          heightCm,
          chestCm,
          visionSpecs,
          priorAttemptsJson
        )
        .run();
      persisted = true;
    } catch (dbErr: any) {
      console.error('D1 profile sync write error:', dbErr);
      return c.json(
        {
          success: false,
          error: 'Database Error',
          message: dbErr.message || 'Failed to persist user profile in D1',
        },
        500
      );
    }
  }

  return c.json(
    {
      success: true,
      status: 'synced',
      user_id: userId,
      persisted_to_d1: persisted,
      synced_at: new Date().toISOString(),
    },
    200
  );
});

// Method Not Allowed Middleware
app.use('/api/v1/*', async (c, next) => {
  const method = c.req.method;
  const path = c.req.path;

  if (method === 'OPTIONS') {
    return next();
  }

  if (path === '/api/v1/profile/evaluate' || path === '/api/v1/profile/sync') {
    if (method !== 'POST') {
      return c.json(
        {
          success: false,
          error: 'Method Not Allowed',
          message: `Method ${method} is not allowed on ${path}. Allowed methods: POST`,
        },
        405
      );
    }
  } else if (path.startsWith('/api/v1/exams') || path.startsWith('/api/v1/syllabus')) {
    if (method !== 'GET') {
      return c.json(
        {
          success: false,
          error: 'Method Not Allowed',
          message: `Method ${method} is not allowed on ${path}. Allowed methods: GET`,
        },
        405
      );
    }
  }

  await next();
});

// 404 Catch-All
app.notFound((c) => {
  return c.json(
    {
      success: false,
      error: 'Not Found',
      message: `Route ${c.req.method} ${c.req.path} not found`,
    },
    404
  );
});

// Global Error Handler
app.onError((err, c) => {
  console.error('Unhandled Worker Exception:', err);
  return c.json(
    {
      success: false,
      error: 'Internal Server Error',
      message: err.message || 'An unexpected server error occurred.',
    },
    500
  );
});

export default app;
