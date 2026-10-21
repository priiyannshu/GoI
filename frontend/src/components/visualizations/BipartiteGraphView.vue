<template>
  <div class="relative w-full h-[700px] bg-slate-900 rounded-2xl border border-slate-800 overflow-hidden select-none flex flex-col">
    <!-- Graph Header / Status Bar -->
    <div class="absolute top-4 left-4 z-10 flex flex-wrap items-center gap-3 pointer-events-none">
      <div class="pointer-events-auto px-3.5 py-1.5 rounded-xl bg-slate-800/90 backdrop-blur-md border border-slate-700/80 shadow-lg flex items-center space-x-2 text-xs">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
        <span class="text-slate-200 font-semibold">Bipartite Force Network</span>
        <span class="text-slate-400">|</span>
        <span class="text-slate-300 font-mono">{{ renderedStats.examCount }} Exams</span>
        <span class="text-slate-500">•</span>
        <span class="text-slate-300 font-mono">{{ renderedStats.topicCount }} Topics</span>
        <span class="text-slate-500">•</span>
        <span class="text-slate-300 font-mono">{{ renderedStats.linkCount }} Links</span>
      </div>

      <!-- Active Intersection Indicator (Cross-View Sync) -->
      <div
        v-if="store.activeIntersectionTopics.length > 0"
        class="pointer-events-auto px-3 py-1.5 rounded-xl bg-indigo-900/80 border border-indigo-500/50 backdrop-blur-md text-xs text-indigo-200 flex items-center space-x-2 shadow-lg"
      >
        <span class="font-bold text-indigo-300">Active Overlap:</span>
        <span>{{ store.pinnedCombinationKey || 'Selected Intersection' }} ({{ store.activeIntersectionTopics.length }} topics)</span>
        <button
          @click="store.clearActiveIntersection()"
          class="ml-1 text-indigo-300 hover:text-white p-0.5 rounded hover:bg-indigo-700/50"
          title="Clear Overlap Filter"
        >
          ✕
        </button>
      </div>
    </div>

    <!-- Graph Canvas SVG Container -->
    <div ref="containerRef" class="w-full h-full relative cursor-grab active:cursor-grabbing">
      <svg ref="svgRef" class="w-full h-full block">
        <defs>
          <!-- Exam Node Drop Shadows -->
          <filter id="exam-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.6" />
          </filter>
          <filter id="topic-highlight-glow" x="-50%" y="-50%" width="200%" height="200%">
            <feDropShadow dx="0" dy="0" stdDeviation="8" flood-color="#38BDF8" flood-opacity="0.8" />
          </filter>
          <filter id="intersection-pulse" x="-50%" y="-50%" width="200%" height="200%">
            <feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#818CF8" flood-opacity="0.9" />
          </filter>

          <!-- Linear Gradients for Edge Highlighting -->
          <linearGradient id="edge-grad-default" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#3B82F6" stop-opacity="0.4" />
            <stop offset="100%" stop-color="#38BDF8" stop-opacity="0.4" />
          </linearGradient>
        </defs>

        <!-- Dynamic Viewport Group (Transformed via D3 Zoom) -->
        <g ref="viewportRef" class="viewport">
          <!-- Edge Layer -->
          <g class="links-layer"></g>

          <!-- Node Layer -->
          <g class="nodes-layer"></g>
        </g>
      </svg>

      <!-- Interactive Hover Tooltip -->
      <transition name="fade">
        <div
          v-if="hoverTooltip.visible && hoverTooltip.data"
          class="absolute z-30 pointer-events-none transform -translate-x-1/2 -translate-y-full mb-3 px-4 py-3 rounded-xl bg-slate-900/95 backdrop-blur-md border border-slate-700 shadow-2xl text-xs text-slate-200 max-w-xs transition-opacity duration-150"
          :style="{ left: `${hoverTooltip.x}px`, top: `${hoverTooltip.y}px` }"
        >
          <!-- Tooltip for Exam Node -->
          <template v-if="hoverTooltip.type === 'exam'">
            <div class="flex items-center justify-between gap-2 border-b border-slate-800 pb-2 mb-2">
              <span class="font-bold text-white text-sm">{{ hoverTooltip.data.short_code }}</span>
              <span
                class="px-2 py-0.5 rounded text-[10px] font-semibold text-white"
                :style="{ backgroundColor: getClusterColor(hoverTooltip.data.category) }"
              >
                {{ hoverTooltip.data.category }}
              </span>
            </div>
            <p class="text-slate-300 font-medium mb-1">{{ hoverTooltip.data.name }}</p>
            <div class="flex items-center justify-between text-[11px] text-slate-400 mt-2">
              <span>Administering Body:</span>
              <span class="text-slate-200 font-medium">{{ hoverTooltip.data.description }}</span>
            </div>
            <div class="flex items-center justify-between text-[11px] text-slate-400 mt-1">
              <span>Active Syllabus Topics:</span>
              <span class="text-emerald-400 font-bold font-mono">{{ hoverTooltip.data.degree }} topics</span>
            </div>
          </template>

          <!-- Tooltip for Topic Node -->
          <template v-else>
            <div class="flex items-center justify-between gap-2 border-b border-slate-800 pb-2 mb-2">
              <span
                class="px-2 py-0.5 rounded text-[10px] font-semibold text-slate-900"
                :style="{ backgroundColor: getDomainColor(hoverTooltip.data.domain) }"
              >
                {{ hoverTooltip.data.domain }}
              </span>
              <span class="text-[10px] text-slate-400 font-mono">{{ hoverTooltip.data.sub_domain }}</span>
            </div>
            <p class="text-white font-bold text-xs mb-1.5 leading-snug">{{ hoverTooltip.data.name }}</p>
            <p class="text-[11px] text-slate-400 line-clamp-2 mb-2">{{ hoverTooltip.data.description }}</p>
            <div class="flex items-center justify-between pt-1 border-t border-slate-800 text-[11px]">
              <span class="text-slate-400">Tested in:</span>
              <span class="text-emerald-400 font-bold font-mono">
                {{ hoverTooltip.data.degree }} / {{ store.selectedExamIds.length }} selected exams
              </span>
            </div>
            <div class="text-[10px] text-slate-500 italic mt-1 text-center">
              Click node to inspect syllabus clauses & depth
            </div>
          </template>
        </div>
      </transition>
    </div>

    <!-- Floating Zoom & Canvas Controls -->
    <div class="absolute bottom-4 right-4 z-20 flex flex-col space-y-2">
      <div class="bg-slate-800/90 backdrop-blur-md border border-slate-700/80 rounded-xl p-1.5 shadow-xl flex flex-col space-y-1">
        <button
          @click="zoomIn"
          class="w-8 h-8 rounded-lg bg-slate-700/60 hover:bg-slate-600 text-slate-200 hover:text-white flex items-center justify-center text-base font-bold transition-colors"
          title="Zoom In"
        >
          +
        </button>
        <button
          @click="zoomOut"
          class="w-8 h-8 rounded-lg bg-slate-700/60 hover:bg-slate-600 text-slate-200 hover:text-white flex items-center justify-center text-base font-bold transition-colors"
          title="Zoom Out"
        >
          −
        </button>
        <button
          @click="resetZoom"
          class="w-8 h-8 rounded-lg bg-slate-700/60 hover:bg-slate-600 text-slate-200 hover:text-white flex items-center justify-center text-xs font-semibold transition-colors"
          title="Reset View (100%)"
        >
          1:1
        </button>
      </div>

      <div class="bg-slate-800/90 backdrop-blur-md border border-slate-700/80 rounded-xl p-1.5 shadow-xl flex flex-col space-y-1">
        <button
          @click="reheatSimulation"
          class="w-8 h-8 rounded-lg bg-slate-700/60 hover:bg-slate-600 text-slate-200 hover:text-white flex items-center justify-center text-xs font-semibold transition-colors"
          title="Reheat Force Physics"
        >
          ⚡
        </button>
        <button
          @click="unpinAllNodes"
          class="w-8 h-8 rounded-lg bg-slate-700/60 hover:bg-slate-600 text-slate-200 hover:text-white flex items-center justify-center text-xs font-semibold transition-colors"
          title="Unpin All Nodes"
        >
          🔓
        </button>
      </div>
    </div>

    <!-- Visual Legend Bar (Bottom Left) -->
    <div class="absolute bottom-4 left-4 z-20 pointer-events-none hidden md:block">
      <div class="pointer-events-auto px-4 py-2.5 rounded-xl bg-slate-800/90 backdrop-blur-md border border-slate-700/80 shadow-xl text-xs space-y-2 max-w-md">
        <!-- Cognitive Depth Legend -->
        <div class="flex items-center space-x-3">
          <span class="text-slate-400 font-semibold text-[11px] uppercase tracking-wider">Depth:</span>
          <div class="flex items-center space-x-1.5 text-[11px] text-slate-300">
            <span class="inline-block w-4 h-[1.5px] bg-slate-400"></span>
            <span>Foundation (1.5px)</span>
          </div>
          <div class="flex items-center space-x-1.5 text-[11px] text-slate-300">
            <span class="inline-block w-4 h-[2.5px] bg-sky-400"></span>
            <span>Inter (2.5px)</span>
          </div>
          <div class="flex items-center space-x-1.5 text-[11px] text-slate-300">
            <span class="inline-block w-4 h-[3.5px] bg-amber-400"></span>
            <span>Adv (3.5px)</span>
          </div>
          <div class="flex items-center space-x-1.5 text-[11px] text-slate-300">
            <span class="inline-block w-4 h-[5.0px] bg-pink-500"></span>
            <span>Analytical (5px)</span>
          </div>
        </div>

        <!-- Domain Legend -->
        <div class="flex flex-wrap items-center gap-x-3 gap-y-1 pt-1.5 border-t border-slate-700/60 text-[10px]">
          <span class="text-slate-400 font-semibold uppercase tracking-wider">Domains:</span>
          <span v-for="(col, dom) in DOMAIN_COLORS" :key="dom" class="flex items-center space-x-1">
            <span class="w-2 h-2 rounded-full" :style="{ backgroundColor: col }"></span>
            <span class="text-slate-300">{{ dom }}</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch, computed, reactive } from 'vue';
import * as d3 from 'd3';
import {
  useSyllabusVisualizationStore,
  DOMAIN_COLORS,
  CLUSTER_COLORS,
} from '@/stores/useSyllabusVisualizationStore';
import type { BipartiteGraphNode, BipartiteGraphLink, DepthLevel } from '@/types/syllabus';

const store = useSyllabusVisualizationStore();

// DOM References
const containerRef = ref<HTMLDivElement | null>(null);
const svgRef = ref<SVGSVGElement | null>(null);
const viewportRef = ref<SVGGElement | null>(null);

// Interactive Hover Tooltip State
const hoverTooltip = reactive({
  visible: false,
  x: 0,
  y: 0,
  type: 'topic' as 'exam' | 'topic',
  data: null as any,
});

// Rendered Counts
const renderedStats = computed(() => {
  const g = store.bipartiteGraphData;
  return {
    examCount: g.nodes.filter((n) => n.type === 'exam').length,
    topicCount: g.nodes.filter((n) => n.type === 'topic').length,
    linkCount: g.links.length,
  };
});

// D3 Instances
let simulation: d3.Simulation<BipartiteGraphNode, BipartiteGraphLink> | null = null;
let zoomBehavior: d3.ZoomBehavior<SVGSVGElement, unknown> | null = null;
let resizeObserver: ResizeObserver | null = null;

// Graph Node & Link Selections
let linkSelection: d3.Selection<SVGLineElement, BipartiteGraphLink, SVGGElement, unknown>;
let nodeSelection: d3.Selection<SVGGElement, BipartiteGraphNode, SVGGElement, unknown>;

// Color Helpers
function getDomainColor(domain?: string): string {
  if (!domain) return '#94A3B8';
  return DOMAIN_COLORS[domain] || '#38BDF8';
}

function getClusterColor(category?: string): string {
  if (!category) return '#3B82F6';
  return CLUSTER_COLORS[category] || '#3B82F6';
}

function getDepthColor(depth: DepthLevel): string {
  switch (depth) {
    case 'Analytical':
      return '#EC4899'; // Pink 500
    case 'Advanced':
      return '#F59E0B'; // Amber 500
    case 'Intermediate':
      return '#38BDF8'; // Sky 400
    case 'Foundation':
    default:
      return '#94A3B8'; // Slate 400
  }
}

// -----------------------------------------------------------------------
// Graph Initialization & Rendering Engine
// -----------------------------------------------------------------------
function renderGraph() {
  if (!svgRef.value || !containerRef.value) return;

  const width = containerRef.value.clientWidth || 900;
  const height = containerRef.value.clientHeight || 700;
  const centerX = width / 2;
  const centerY = height / 2;

  const svg = d3.select(svgRef.value);
  const viewport = d3.select(viewportRef.value);
  const linksLayer = viewport.select<SVGGElement>('.links-layer');
  const nodesLayer = viewport.select<SVGGElement>('.nodes-layer');

  // Configure Zoom with Clamped Boundaries [0.2, 5.0] (test_f20_zoom_and_pan_transform_boundaries)
  zoomBehavior = d3
    .zoom<SVGSVGElement, unknown>()
    .scaleExtent([0.2, 5.0])
    .on('zoom', (event) => {
      viewport.attr('transform', event.transform);
    });

  svg.call(zoomBehavior);

  // Map of previously positioned nodes to maintain coordinate stability across filter/intersection changes
  const prevNodesMap = new Map<string, BipartiteGraphNode>();
  if (simulation) {
    simulation.nodes().forEach((n) => prevNodesMap.set(n.id, n));
    simulation.stop();
  }

  // Clone data to avoid mutating store reactivity directly in simulation
  const rawData = store.bipartiteGraphData;
  const nodes: BipartiteGraphNode[] = rawData.nodes.map((n) => ({ ...n }));
  const links: BipartiteGraphLink[] = rawData.links.map((l) => ({ ...l }));

  // Distribute positions:
  // Exams evenly on outer radial ring (radius = 340) (test_f20_radial_separation_exams_outer_topics_inner)
  const examNodes = nodes.filter((n) => n.type === 'exam');
  const examCount = examNodes.length;
  examNodes.forEach((node, i) => {
    const prev = prevNodesMap.get(node.id);
    if (prev && prev.x !== undefined && prev.y !== undefined) {
      node.x = prev.x;
      node.y = prev.y;
      node.vx = prev.vx;
      node.vy = prev.vy;
      node.fx = prev.fx !== undefined ? prev.fx : prev.x;
      node.fy = prev.fy !== undefined ? prev.fy : prev.y;
    } else {
      const angle = (2 * Math.PI * i) / Math.max(1, examCount) - Math.PI / 2;
      node.x = centerX + 340 * Math.cos(angle);
      node.y = centerY + 340 * Math.sin(angle);
      // Pin initial exam coordinates slightly to anchor clusters
      node.fx = node.x;
      node.fy = node.y;
    }
  });

  // Topics clustered inside inner zone (radius = 140)
  const topicNodes = nodes.filter((n) => n.type === 'topic');
  topicNodes.forEach((node, i) => {
    const prev = prevNodesMap.get(node.id);
    if (prev && prev.x !== undefined && prev.y !== undefined) {
      node.x = prev.x;
      node.y = prev.y;
      node.vx = prev.vx;
      node.vy = prev.vy;
      node.fx = prev.fx;
      node.fy = prev.fy;
    } else {
      const angle = (2 * Math.PI * i) / Math.max(1, topicNodes.length);
      const rad = 60 + Math.random() * 100;
      node.x = centerX + rad * Math.cos(angle);
      node.y = centerY + rad * Math.sin(angle);
    }
  });

  // Setup D3 Force Simulation
  // Parameters: charge_exam = -800, charge_topic = -150, collision = 16, alpha_decay = 0.04
  // (test_f20_force_simulation_parameters_configured, test_f20_simulation_tick_alpha_decay_terminates)
  simulation = d3
    .forceSimulation<BipartiteGraphNode, BipartiteGraphLink>(nodes)
    .alphaDecay(0.04)
    .force(
      'link',
      d3
        .forceLink<BipartiteGraphNode, BipartiteGraphLink>(links)
        .id((d) => d.id)
        .distance((d) => {
          const targetNode = d.target as BipartiteGraphNode;
          return targetNode.type === 'topic' ? 140 : 180;
        })
        .strength(0.35)
    )
    .force(
      'charge',
      d3.forceManyBody<BipartiteGraphNode>().strength((d) => {
        return d.type === 'exam' ? -800 : -150;
      })
    )
    .force(
      'collide',
      d3.forceCollide<BipartiteGraphNode>().radius((d) => Math.max(16, d.r + 6)).iterations(2)
    )
    .force(
      'radial',
      d3
        .forceRadial<BipartiteGraphNode>(
          (d) => (d.type === 'exam' ? 340 : 140),
          centerX,
          centerY
        )
        .strength((d) => (d.type === 'exam' ? 0.6 : 0.2))
    )
    .force('center', d3.forceCenter(centerX, centerY).strength(0.04));

  // -------------------------------------------------------------
  // Render Links
  // -------------------------------------------------------------
  linksLayer.selectAll('*').remove();
  linkSelection = linksLayer
    .selectAll<SVGLineElement, BipartiteGraphLink>('line')
    .data(links)
    .enter()
    .append('line')
    .attr('class', 'bipartite-link')
    .attr('stroke', (d) => getDepthColor(d.depth_level))
    .attr('stroke-width', (d) => d.stroke_width)
    .attr('stroke-opacity', (d) => {
      if (store.activeIntersectionTopics.length > 0) {
        const targetId = typeof d.target === 'object' ? (d.target as any).id : d.target;
        return store.activeIntersectionTopics.includes(targetId) ? 0.85 : 0.15;
      }
      return 0.4;
    })
    .attr('stroke-linecap', 'round')
    .attr('stroke-dasharray', (d) => (d.depth_level === 'Foundation' ? '3 2' : 'none'));

  // -------------------------------------------------------------
  // Render Nodes
  // -------------------------------------------------------------
  nodesLayer.selectAll('*').remove();
  nodeSelection = nodesLayer
    .selectAll<SVGGElement, BipartiteGraphNode>('g')
    .data(nodes)
    .enter()
    .append('g')
    .attr('class', (d) => `node-group node-${d.type}`)
    .call(
      d3
        .drag<SVGGElement, BipartiteGraphNode>()
        .on('start', dragStarted)
        .on('drag', dragged)
        .on('end', dragEnded)
    );

  // Render Exam Nodes (Radius = 32px, Cluster color, Short Code, Topic Count Badge)
  const examGroups = nodeSelection.filter((d) => d.type === 'exam');

  examGroups
    .append('circle')
    .attr('r', (d) => d.r)
    .attr('fill', (d) => getClusterColor(d.category))
    .attr('stroke', '#0F172A')
    .attr('stroke-width', 3)
    .attr('filter', 'url(#exam-glow)')
    .attr('cursor', 'pointer');

  examGroups
    .append('text')
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'central')
    .attr('fill', '#FFFFFF')
    .attr('font-size', '11px')
    .attr('font-weight', '700')
    .attr('pointer-events', 'none')
    .text((d) => d.short_code || d.id);

  // Degree badge for exam node
  const examBadges = examGroups
    .append('g')
    .attr('transform', (d) => `translate(0, ${d.r + 14})`)
    .attr('pointer-events', 'none');

  examBadges
    .append('rect')
    .attr('x', -24)
    .attr('y', -8)
    .attr('width', 48)
    .attr('height', 16)
    .attr('rx', 8)
    .attr('fill', '#1E293B')
    .attr('stroke', '#334155')
    .attr('stroke-width', 1);

  examBadges
    .append('text')
    .attr('text-anchor', 'middle')
    .attr('dominant-baseline', 'central')
    .attr('fill', '#38BDF8')
    .attr('font-size', '9px')
    .attr('font-weight', '600')
    .text((d) => `${d.degree} t`);

  // Render Topic Nodes (Radius = 12 + sqrt(degree) * 3, Domain color)
  const topicGroups = nodeSelection.filter((d) => d.type === 'topic');

  topicGroups
    .append('circle')
    .attr('r', (d) => d.r)
    .attr('fill', (d) => getDomainColor(d.domain))
    .attr('stroke', '#0F172A')
    .attr('stroke-width', 1.5)
    .attr('cursor', 'pointer')
    .attr('opacity', (d) => {
      if (store.activeIntersectionTopics.length > 0) {
        return store.activeIntersectionTopics.includes(d.id) ? 1.0 : 0.35;
      }
      return 1.0;
    });

  // Pulsing ring for topics matching cross-view active intersection
  topicGroups
    .filter((d) => store.activeIntersectionTopics.includes(d.id))
    .append('circle')
    .attr('r', (d) => d.r + 4)
    .attr('fill', 'none')
    .attr('stroke', '#818CF8')
    .attr('stroke-width', 2.5)
    .attr('stroke-dasharray', '4 2')
    .attr('filter', 'url(#intersection-pulse)');

  // Topic Labels (conditionally visible or on zoom)
  topicGroups
    .append('text')
    .attr('class', 'topic-label')
    .attr('x', (d) => d.r + 4)
    .attr('y', 3)
    .attr('fill', '#94A3B8')
    .attr('font-size', '9px')
    .attr('font-weight', '500')
    .attr('pointer-events', 'none')
    .text((d) => (d.name.length > 20 ? d.name.slice(0, 18) + '…' : d.name))
    .style('opacity', (d) => (d.degree >= 2 ? 0.9 : 0.4));

  // -------------------------------------------------------------
  // Interactive Hover & Click Listeners
  // -------------------------------------------------------------
  nodeSelection
    .on('mouseenter', (event: MouseEvent, d: BipartiteGraphNode) => {
      handleNodeHover(d, event);
    })
    .on('mouseleave', () => {
      handleNodeLeave();
    })
    .on('click', (event: MouseEvent, d: BipartiteGraphNode) => {
      event.stopPropagation();
      if (d.type === 'topic') {
        store.setSelectedTopic(d.id);
      } else {
        store.setHoveredExam(d.id);
      }
    })
    .on('dblclick', (event: MouseEvent, d: BipartiteGraphNode) => {
      // Double click unpins node coordinates (test_f20_node_drag_pins_and_unpins_coordinates)
      event.stopPropagation();
      d.fx = null;
      d.fy = null;
      simulation?.alpha(0.15).restart();
    });

  // -------------------------------------------------------------
  // Simulation Tick Handler
  // -------------------------------------------------------------
  simulation.on('tick', () => {
    linkSelection
      .attr('x1', (d) => (d.source as BipartiteGraphNode).x || 0)
      .attr('y1', (d) => (d.source as BipartiteGraphNode).y || 0)
      .attr('x2', (d) => (d.target as BipartiteGraphNode).x || 0)
      .attr('y2', (d) => (d.target as BipartiteGraphNode).y || 0);

    nodeSelection.attr('transform', (d) => `translate(${d.x || 0}, ${d.y || 0})`);
  });
}

// -----------------------------------------------------------------------
// Drag Dynamics (Pins fx, fy on drag; unpins or keeps on drop)
// -----------------------------------------------------------------------
function dragStarted(event: d3.D3DragEvent<SVGGElement, BipartiteGraphNode, BipartiteGraphNode>, d: BipartiteGraphNode) {
  if (!event.active && simulation) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(event: d3.D3DragEvent<SVGGElement, BipartiteGraphNode, BipartiteGraphNode>, d: BipartiteGraphNode) {
  d.fx = event.x;
  d.fy = event.y;
}

function dragEnded(event: d3.D3DragEvent<SVGGElement, BipartiteGraphNode, BipartiteGraphNode>, d: BipartiteGraphNode) {
  if (!event.active && simulation) simulation.alphaTarget(0);
}

// -----------------------------------------------------------------------
// Hover Highlighting & Background Dimming Engine
// -----------------------------------------------------------------------
function handleNodeHover(node: BipartiteGraphNode, event: MouseEvent) {
  const container = containerRef.value;
  if (!container) return;

  const rect = container.getBoundingClientRect();
  hoverTooltip.x = event.clientX - rect.left;
  hoverTooltip.y = event.clientY - rect.top;
  hoverTooltip.type = node.type;
  hoverTooltip.data = node;
  hoverTooltip.visible = true;

  if (node.type === 'exam') {
    store.setHoveredExam(node.id);
  } else {
    store.setHoveredTopic(node.id);
  }

  // Find incident edges and neighbor IDs
  const neighborIds = new Set<string>([node.id]);

  linkSelection.each(function (l) {
    const sId = (l.source as BipartiteGraphNode).id;
    const tId = (l.target as BipartiteGraphNode).id;
    const isIncident = sId === node.id || tId === node.id;

    if (isIncident) {
      neighborIds.add(sId);
      neighborIds.add(tId);
      d3.select(this)
        .transition()
        .duration(100)
        .attr('stroke-opacity', 0.95)
        .attr('stroke-width', l.stroke_width + 1.5);
    } else {
      d3.select(this)
        .transition()
        .duration(100)
        .attr('stroke-opacity', 0.05);
    }
  });

  nodeSelection.each(function (n) {
    const isNeighbor = neighborIds.has(n.id);
    d3.select(this)
      .transition()
      .duration(100)
      .style('opacity', isNeighbor ? 1.0 : 0.12)
      .attr('transform', `translate(${n.x || 0}, ${n.y || 0}) scale(${isNeighbor ? 1.15 : 0.95})`);
  });
}

function handleNodeLeave() {
  hoverTooltip.visible = false;
  hoverTooltip.data = null;
  store.setHoveredExam(null);
  store.setHoveredTopic(null); // (test_f21_hover_cleared_on_mouse_leave)

  // Reset opacities and stroke widths
  if (linkSelection) {
    linkSelection
      .transition()
      .duration(150)
      .attr('stroke-opacity', 0.4)
      .attr('stroke-width', (d) => d.stroke_width);
  }

  if (nodeSelection) {
    nodeSelection
      .transition()
      .duration(150)
      .style('opacity', 1.0)
      .attr('transform', (n) => `translate(${n.x || 0}, ${n.y || 0}) scale(1)`);
  }
}

// -----------------------------------------------------------------------
// Canvas Control Actions (Zoom, Reheat, Unpin)
// -----------------------------------------------------------------------
function zoomIn() {
  if (!svgRef.value || !zoomBehavior) return;
  d3.select(svgRef.value).transition().duration(250).call(zoomBehavior.scaleBy, 1.3);
}

function zoomOut() {
  if (!svgRef.value || !zoomBehavior) return;
  d3.select(svgRef.value).transition().duration(250).call(zoomBehavior.scaleBy, 0.77);
}

function resetZoom() {
  if (!svgRef.value || !zoomBehavior) return;
  d3.select(svgRef.value).transition().duration(300).call(zoomBehavior.transform, d3.zoomIdentity);
}

function reheatSimulation() {
  if (!simulation) return;
  simulation.alpha(0.6).restart();
}

function unpinAllNodes() {
  const rawData = store.bipartiteGraphData;
  rawData.nodes.forEach((n) => {
    n.fx = null;
    n.fy = null;
  });
  if (nodeSelection) {
    nodeSelection.each((d) => {
      d.fx = null;
      d.fy = null;
    });
  }
  reheatSimulation();
}

// -----------------------------------------------------------------------
// Lifecycle & Reactive Watchers
// -----------------------------------------------------------------------
onMounted(async () => {
  await store.loadSyllabusData();
  renderGraph();

  if (containerRef.value) {
    resizeObserver = new ResizeObserver(() => {
      renderGraph();
    });
    resizeObserver.observe(containerRef.value);
  }
});

onUnmounted(() => {
  if (simulation) simulation.stop();
  if (resizeObserver) resizeObserver.disconnect();
});

// Watch for dataset or filter changes
watch(
  [
    () => store.selectedExamIds,
    () => store.selectedDomain,
    () => store.minDepthLevel,
    () => store.searchQuery,
    () => store.activeIntersectionTopics,
  ],
  () => {
    renderGraph();
  },
  { deep: true }
);
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
