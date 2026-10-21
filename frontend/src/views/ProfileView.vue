<template>
  <div class="space-y-6 pb-16">
    <!-- Profile View Header & Tabs -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">Candidate Profile & Statutory Eligibility</h1>
      </div>

      <div class="flex flex-wrap items-center gap-2">
        <!-- Save Profile Button -->
        <button
          @click="saveProfile"
          :disabled="isSavingProfile"
          class="inline-flex items-center space-x-1.5 py-1.5 px-3.5 rounded-xl text-xs font-bold transition-all shadow-sm bg-emerald-600 hover:bg-emerald-500 text-white disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
        >
          <svg v-if="isSavingProfile" class="animate-spin h-3.5 w-3.5 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
          </svg>
          <span>{{ isSavingProfile ? 'Saving...' : 'Save Profile' }}</span>
        </button>

        <!-- Tab Switcher -->
        <div class="flex rounded-xl bg-slate-100 dark:bg-slate-800 p-1 border border-slate-200 dark:border-slate-700/80">
          <button
            @click="activeTab = 'profile'"
            class="py-1.5 px-4 rounded-lg text-xs font-semibold transition-all cursor-pointer"
            :class="activeTab === 'profile' ? 'bg-emerald-500 text-white shadow' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
          >
            👤 My Profile
          </button>
          <button
            @click="activeTab = 'summary'"
            class="py-1.5 px-4 rounded-lg text-xs font-semibold transition-all flex items-center space-x-1.5 cursor-pointer"
            :class="activeTab === 'summary' ? 'bg-emerald-500 text-white shadow' : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-white'"
          >
            <span>🎯 Eligibility Summary</span>
            <span
              v-if="eligibilityStore.eligibleCount > 0"
              class="px-1.5 py-0.2 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40"
            >
              {{ eligibilityStore.eligibleCount }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- TAB 1: MY PROFILE (INDIVIDUAL SKIPPABLE FIELDS) -->
    <div v-if="activeTab === 'profile'" class="space-y-6">
      <!-- Profile Completion Gauge -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 sm:p-5 shadow-sm dark:shadow-lg">
        <div class="space-y-1">
          <div class="flex items-center space-x-2">
            <span class="text-xs font-bold text-slate-700 dark:text-white uppercase tracking-wider">Profile Completeness</span>
            <span class="text-xs font-mono font-bold text-emerald-500 dark:text-emerald-400">{{ profileStore.completionPercentage }}%</span>
          </div>
          <div class="w-full sm:w-80 h-2 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden">
            <div
              class="h-full bg-emerald-500 transition-all duration-500"
              :style="{ width: `${profileStore.completionPercentage}%` }"
            ></div>
          </div>
        </div>
      </div>

      <!-- SECTION 1: CANDIDATE IDENTITY & DEMOGRAPHICS -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm dark:shadow-lg space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
          <div class="flex items-center space-x-2">
            <span class="text-lg">🆔</span>
            <h3 class="text-base font-bold text-slate-900 dark:text-white">Candidate Identity & Demographics</h3>
          </div>
        </div>

        <!-- Full Name -->
        <div>
          <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Candidate Full Name</label>
          <input
            type="text"
            v-model="profile.full_name"
            placeholder="e.g. Priyanshu Kumar"
            class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3.5 py-2 text-sm text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 focus:outline-none focus:border-emerald-500"
          />
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <!-- DOB -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Date of Birth</label>
            <input
              type="date"
              v-model="profile.dob"
              class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3.5 py-2 text-sm text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
            />
            <p class="text-[11px] text-slate-500 mt-1">Calculates age against 2027 statutory reference cutoff dates.</p>
          </div>

          <!-- Calculated Age Badges -->
          <div class="bg-slate-50 dark:bg-slate-850 border border-slate-200 dark:border-slate-800 rounded-xl p-3 flex items-center justify-around text-center">
            <div>
              <span class="text-xs text-slate-500 dark:text-slate-400 block">Aug 1, 2027 (UPSC)</span>
              <span class="text-lg font-bold font-mono text-emerald-500 dark:text-emerald-400">
                {{ profile.dob ? `${profileStore.calculatedAge2027Aug1} yrs` : '—' }}
              </span>
            </div>
            <div class="w-px h-8 bg-slate-200 dark:bg-slate-750"></div>
            <div>
              <span class="text-xs text-slate-500 dark:text-slate-400 block">Jan 1, 2027 (ESE)</span>
              <span class="text-lg font-bold font-mono text-sky-500 dark:text-sky-400">
                {{ profile.dob ? `${profileStore.calculatedAge2027Jan1} yrs` : '—' }}
              </span>
            </div>
            <div class="w-px h-8 bg-slate-200 dark:bg-slate-750"></div>
            <div>
              <span class="text-xs text-slate-500 dark:text-slate-400 block">Jul 1, 2027 (State)</span>
              <span class="text-lg font-bold font-mono text-purple-500 dark:text-purple-400">
                {{ profile.dob ? `${profileStore.calculatedAge2027Jul1} yrs` : '—' }}
              </span>
            </div>
          </div>
        </div>

        <!-- Gender & Category -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 pt-2">
          <!-- Gender -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Gender</label>
            <div class="grid grid-cols-3 gap-2">
              <button
                v-for="g in ['Male', 'Female', 'Other']"
                :key="g"
                type="button"
                @click="profile.gender = (profile.gender === g ? ('' as any) : (g as any))"
                class="py-2 px-3 rounded-xl text-xs font-semibold border transition-all"
                :class="profile.gender === g ? 'bg-emerald-500 text-white border-emerald-500' : 'bg-slate-100 dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-750'"
              >
                {{ g }}
              </button>
            </div>
          </div>

          <!-- Social Category -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Reservation Category</label>
            <select
              v-model="profile.category"
              class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3.5 py-2 text-sm text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
            >
              <option value="">Select Social Category</option>
              <option value="GEN">General (UR)</option>
              <option value="EWS">Economically Weaker Section (EWS)</option>
              <option value="OBC">Other Backward Classes (OBC-NCL)</option>
              <option value="SC">Scheduled Caste (SC)</option>
              <option value="ST">Scheduled Tribe (ST)</option>
              <option value="PWBD_GEN">PwBD - General (10 yrs relaxation)</option>
              <option value="PWBD_OBC">PwBD - OBC (13 yrs relaxation)</option>
              <option value="PWBD_SC_ST">PwBD - SC/ST (15 yrs relaxation)</option>
            </select>
          </div>
        </div>
      </div>

      <!-- SECTION 2: ACADEMICS -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm dark:shadow-lg space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
          <div class="flex items-center space-x-2">
            <span class="text-lg">🎓</span>
            <h3 class="text-base font-bold text-slate-900 dark:text-white">Academic Qualifications</h3>
          </div>
        </div>

        <div class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <!-- Degree Level -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Degree Level</label>
              <select
                v-model="profile.graduation_degree"
                class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
              >
                <option value="">Select Degree Level</option>
                <option value="Bachelor">Bachelor Degree (B.A., B.Sc., B.Tech, etc.)</option>
                <option value="Master">Master Degree (M.A., M.Sc., M.Tech, etc.)</option>
                <option value="Dual_UG_and_MBA">Dual UG and MBA / Professional</option>
              </select>
            </div>

            <!-- Discipline -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Discipline / Branch</label>
              <select
                v-model="profile.graduation_discipline"
                class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
              >
                <option value="">Select Discipline / Branch</option>
                <option value="ANY">Any / General Graduate</option>
                <option value="Geoinformatics">Geoinformatics / Remote Sensing / GIS</option>
                <option value="Civil">Civil Engineering</option>
                <option value="Mechanical">Mechanical Engineering</option>
                <option value="Electrical">Electrical Engineering</option>
                <option value="Electronics">Electronics & Telecom</option>
                <option value="Computer_Science">Computer Science & IT</option>
                <option value="Chemical">Chemical Engineering</option>
                <option value="Economics">Economics / Finance</option>
                <option value="Commerce">Commerce / B.Com / M.Com</option>
                <option value="CA">Chartered Accountant (CA / ICAI)</option>
                <option value="CFA">Chartered Financial Analyst (CFA)</option>
                <option value="Law">Law (LL.B / B.A. LL.B)</option>
                <option value="Statistics">Statistics / Mathematical Statistics</option>
                <option value="Geology">Geology / Geophysics</option>
                <option value="Physics">Physics / Applied Physics</option>
                <option value="Chemistry">Chemistry</option>
                <option value="Agriculture">Agriculture & Allied</option>
              </select>
            </div>

            <!-- Aggregate Percentage -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Graduation Aggregate %</label>
              <input
                type="number"
                step="0.01"
                min="35"
                max="100"
                v-model.number="profile.graduation_aggregate_pct"
                placeholder="e.g. 65.50"
                class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
              />
              <span class="text-[10px] text-slate-500">Strict non-rounding (e.g. 59.99% &lt; 60%)</span>
            </div>
          </div>


          <!-- Final Year Toggle & 10+2 Marks -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2 border-t border-slate-200 dark:border-slate-800 items-center">
            <label class="flex items-center space-x-2 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                v-model="profile.is_final_year"
                class="rounded border-slate-300 dark:border-slate-700 text-emerald-500 focus:ring-0"
              />
              <span>Currently in Final Year of Graduation</span>
            </label>

            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">10+2 Maths % (AFCAT/Defense)</label>
              <input
                type="number"
                step="0.1"
                v-model.number="profile.ten_plus_two_maths_pct"
                placeholder="Optional (min 50% for Flying)"
                class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
              />
            </div>

            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1">10+2 Physics % (AFCAT/Defense)</label>
              <input
                type="number"
                step="0.1"
                v-model.number="profile.ten_plus_two_physics_pct"
                placeholder="Optional (min 50% for Flying)"
                class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- SECTION 3: DOMICILE & LANGUAGES -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm dark:shadow-lg space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
          <div class="flex items-center space-x-2">
            <span class="text-lg">🗺️</span>
            <h3 class="text-base font-bold text-slate-900 dark:text-white">Home State Domicile & Regional Languages</h3>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Home State Domicile (All 28 States & 8 UTs)</label>
            <select
              v-model="profile.state_domicile"
              class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3.5 py-2 text-sm text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
            >
              <option value="">Select your Home State / UT</option>
              <optgroup label="States (28)">
                <option value="Andhra Pradesh">Andhra Pradesh</option>
                <option value="Arunachal Pradesh">Arunachal Pradesh</option>
                <option value="Assam">Assam</option>
                <option value="Bihar">Bihar</option>
                <option value="Chhattisgarh">Chhattisgarh</option>
                <option value="Goa">Goa</option>
                <option value="Gujarat">Gujarat</option>
                <option value="Haryana">Haryana</option>
                <option value="Himachal Pradesh">Himachal Pradesh</option>
                <option value="Jharkhand">Jharkhand</option>
                <option value="Karnataka">Karnataka</option>
                <option value="Kerala">Kerala</option>
                <option value="Madhya Pradesh">Madhya Pradesh</option>
                <option value="Maharashtra">Maharashtra</option>
                <option value="Manipur">Manipur</option>
                <option value="Meghalaya">Meghalaya</option>
                <option value="Mizoram">Mizoram</option>
                <option value="Nagaland">Nagaland</option>
                <option value="Odisha">Odisha</option>
                <option value="Punjab">Punjab</option>
                <option value="Rajasthan">Rajasthan</option>
                <option value="Sikkim">Sikkim</option>
                <option value="Tamil Nadu">Tamil Nadu</option>
                <option value="Telangana">Telangana</option>
                <option value="Tripura">Tripura</option>
                <option value="Uttar Pradesh">Uttar Pradesh</option>
                <option value="Uttarakhand">Uttarakhand</option>
                <option value="West Bengal">West Bengal</option>
              </optgroup>
              <optgroup label="Union Territories (8)">
                <option value="Andaman and Nicobar Islands">Andaman and Nicobar Islands</option>
                <option value="Chandigarh">Chandigarh</option>
                <option value="Dadra and Nagar Haveli and Daman and Diu">Dadra and Nagar Haveli and Daman and Diu</option>
                <option value="Delhi">Delhi (NCT)</option>
                <option value="Jammu and Kashmir">Jammu and Kashmir</option>
                <option value="Ladakh">Ladakh</option>
                <option value="Lakshadweep">Lakshadweep</option>
                <option value="Puducherry">Puducherry</option>
              </optgroup>
            </select>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Fluent Regional Languages</label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="lang in ['Hindi', 'English', 'Marathi', 'Bengali', 'Kannada', 'Tamil', 'Telugu', 'Nepali', 'Gujarati', 'Odia', 'Punjabi', 'Assamese', 'Malayalam']"
                :key="lang"
                type="button"
                @click="toggleLanguage(lang)"
                class="px-2.5 py-1 rounded-lg text-xs font-medium border transition-colors"
                :class="profile.fluent_languages?.includes(lang) ? 'bg-emerald-500/20 border-emerald-500/50 text-emerald-600 dark:text-emerald-300 font-bold' : 'bg-slate-100 dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'"
              >
                {{ lang }} {{ profile.fluent_languages?.includes(lang) ? '✓' : '' }}
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- SECTION 4: PHYSICAL STANDARDS -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-6 shadow-sm dark:shadow-lg space-y-5">
        <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
          <div class="flex items-center space-x-2">
            <span class="text-lg">🏃</span>
            <h3 class="text-base font-bold text-slate-900 dark:text-white">Physical & Medical Standards</h3>
          </div>
          <span class="text-xs text-slate-500 dark:text-slate-400">Relevant for CAPF, Defense & Police Cadres</span>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Standing Height (cm)</label>
            <input
              type="number"
              v-model.number="profile.height_cm"
              placeholder="e.g. 170 (optional)"
              class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
            />
            <span class="text-[10px] text-slate-500">Aviation (162.5cm) / Uniformed</span>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Weight (kg)</label>
            <input
              type="number"
              v-model.number="profile.weight_kg"
              placeholder="e.g. 65 (optional)"
              class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
            />
            <span class="text-[10px] text-slate-500">CAPF AC / State Police standard</span>
          </div>

          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-300 mb-1.5">Chest (cm, Unexpanded)</label>
            <input
              type="number"
              v-model.number="profile.chest_cm"
              placeholder="e.g. 84 (optional)"
              class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-emerald-500"
            />
            <span class="text-[10px] text-slate-500">Male uniformed: min 81–84 cm</span>
          </div>

          <div class="flex items-center space-x-3 pt-4">
            <label class="flex items-center space-x-2 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
              <input
                type="checkbox"
                v-model="profile.has_color_blindness"
                class="rounded border-slate-300 dark:border-slate-700 text-emerald-500 focus:ring-0"
              />
              <span>Color Blindness</span>
            </label>
          </div>
        </div>

        <!-- Cockpit Anthropometrics (IAF AFCAT & CDS Flying) -->
        <div class="mt-4 pt-4 border-t border-slate-200 dark:border-slate-800">
          <span class="text-xs font-bold text-sky-700 dark:text-sky-400 block mb-2">✈️ Cockpit Anthropometrics (AFCAT & CDS Flying Branch)</span>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label class="block text-[11px] font-medium text-slate-600 dark:text-slate-400 mb-1">Sitting Height (cm)</label>
              <input
                type="number"
                step="0.5"
                v-model.number="profile.sitting_height_cm"
                placeholder="81.5 – 96.0 cm"
                class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-sky-500"
              />
              <span class="text-[10px] text-slate-500">Cockpit canopy & seat clearance</span>
            </div>
            <div>
              <label class="block text-[11px] font-medium text-slate-600 dark:text-slate-400 mb-1">Leg Length (cm)</label>
              <input
                type="number"
                step="0.5"
                v-model.number="profile.leg_length_cm"
                placeholder="99.0 – 120.0 cm"
                class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-sky-500"
              />
              <span class="text-[10px] text-slate-500">Rudder pedal full throw reach</span>
            </div>
            <div>
              <label class="block text-[11px] font-medium text-slate-600 dark:text-slate-400 mb-1">Thigh Length (cm)</label>
              <input
                type="number"
                step="0.5"
                v-model.number="profile.thigh_length_cm"
                placeholder="Max 64.0 cm"
                class="w-full bg-slate-50 dark:bg-slate-800 border border-slate-300 dark:border-slate-700 rounded-xl px-3 py-1.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:border-sky-500"
              />
              <span class="text-[10px] text-slate-500">Ejection clearance threshold</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Save Action Bar -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl border border-slate-200 dark:border-slate-800 p-4 sm:p-5 shadow-sm dark:shadow-lg flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center space-x-2 text-xs text-slate-600 dark:text-slate-400">
          <span v-if="saveMessage" class="font-medium text-emerald-600 dark:text-emerald-400 flex items-center space-x-1.5">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span>{{ saveMessage }}</span>
          </span>
          <span v-else-if="profileStore.syncStatus === 'synced_online'" class="text-emerald-600 dark:text-emerald-400">
            ✓ Synced to cloud
          </span>
          <span v-else>
            Changes save automatically to local storage and sync online when ready.
          </span>
        </div>

        <button
          @click="saveProfile"
          :disabled="isSavingProfile"
          class="w-full sm:w-auto inline-flex items-center justify-center space-x-2 py-2.5 px-6 rounded-xl text-sm font-bold transition-all shadow-sm bg-emerald-600 hover:bg-emerald-500 text-white disabled:opacity-60 disabled:cursor-not-allowed cursor-pointer"
        >
          <svg v-if="isSavingProfile" class="animate-spin h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <svg v-else class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
          </svg>
          <span>{{ isSavingProfile ? 'Saving...' : 'Save Profile' }}</span>
        </button>
      </div>
    </div>

    <!-- TAB 2: ELIGIBILITY SUMMARY REPORT (NO CONDITIONAL TIER) -->
    <div v-else-if="activeTab === 'summary'" class="space-y-6">
      <!-- 3-Tier Metrics Row: Eligible, Needs Info, Ineligible (compact single-line) -->
      <div class="grid grid-cols-3 gap-2 sm:gap-3">
        <div
          @click="statusFilter = 'ELIGIBLE'"
          class="p-2 sm:p-2.5 rounded-xl bg-emerald-50 dark:bg-emerald-950/20 border border-emerald-300 dark:border-emerald-500/30 cursor-pointer hover:border-emerald-500 transition-all text-center shadow-xs"
          :class="statusFilter === 'ELIGIBLE' ? 'ring-2 ring-emerald-500' : ''"
        >
          <span class="text-[10px] sm:text-xs uppercase font-bold text-emerald-700 dark:text-emerald-400 block truncate">Eligible</span>
          <span class="text-lg sm:text-2xl font-extrabold text-slate-900 dark:text-white font-mono leading-tight block">{{ eligibilityStore.eligibleCount }}</span>
        </div>

        <div
          @click="statusFilter = 'NEEDS_INFO'"
          class="p-2 sm:p-2.5 rounded-xl bg-amber-50 dark:bg-amber-950/20 border border-amber-300 dark:border-amber-500/30 cursor-pointer hover:border-amber-500 transition-all text-center shadow-xs"
          :class="statusFilter === 'NEEDS_INFO' ? 'ring-2 ring-amber-500' : ''"
        >
          <span class="text-[10px] sm:text-xs uppercase font-bold text-amber-700 dark:text-amber-400 block truncate">Missing Info</span>
          <span class="text-lg sm:text-2xl font-extrabold text-slate-900 dark:text-white font-mono leading-tight block">{{ eligibilityStore.needsInfoCount }}</span>
        </div>

        <div
          @click="statusFilter = 'INELIGIBLE'"
          class="p-2 sm:p-2.5 rounded-xl bg-rose-50 dark:bg-rose-950/20 border border-rose-300 dark:border-rose-500/30 cursor-pointer hover:border-rose-500 transition-all text-center shadow-xs"
          :class="statusFilter === 'INELIGIBLE' ? 'ring-2 ring-rose-500' : ''"
        >
          <span class="text-[10px] sm:text-xs uppercase font-bold text-rose-700 dark:text-rose-400 block truncate">Ineligible</span>
          <span class="text-lg sm:text-2xl font-extrabold text-slate-900 dark:text-white font-mono leading-tight block">{{ eligibilityStore.ineligibleCount }}</span>
        </div>
      </div>

      <!-- Empty Profile Warning Banner if 0 fields filled -->
      <div
        v-if="profileStore.completionPercentage === 0"
        class="p-5 rounded-2xl bg-amber-50 dark:bg-amber-950/30 border border-amber-300 dark:border-amber-500/40 text-amber-900 dark:text-amber-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4"
      >
        <div class="space-y-1">
          <div class="font-bold text-sm flex items-center space-x-2">
            <span>ℹ️</span>
            <span>Your candidate profile is currently empty.</span>
          </div>
          <p class="text-xs text-amber-800 dark:text-amber-300">
            Eligibility cannot be computed until you fill in your Date of Birth, Qualification, and Category under the My Profile tab.
          </p>
        </div>
        <button
          @click="activeTab = 'profile'"
          class="self-start sm:self-auto px-4 py-2 rounded-xl text-xs font-bold bg-amber-600 hover:bg-amber-700 text-white transition-colors"
        >
          Fill Profile Now →
        </button>
      </div>

      <!-- Filter / Search Row -->
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div class="flex items-center space-x-2 text-xs">
          <span class="text-slate-500 dark:text-slate-400">Showing:</span>
          <span class="px-2.5 py-1 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-800 dark:text-white font-semibold">
            {{ statusFilter === 'ALL' ? 'All Audited Examinations' : formatStatus(statusFilter) }}
          </span>
          <button
            v-if="statusFilter !== 'ALL'"
            @click="statusFilter = 'ALL'"
            class="text-xs text-slate-500 hover:text-slate-900 dark:hover:text-white underline ml-2"
          >
            Show All
          </button>
        </div>

        <div class="text-xs text-slate-500 dark:text-slate-400">
          Click any card to inspect full statutory rules, syllabus & 2027 dates
        </div>
      </div>

      <!-- Verdict Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="verdict in summaryVerdicts"
          :key="verdict.exam_id"
          @click="router.push(`/exams/${verdict.exam_id}`)"
          class="p-4 rounded-xl bg-white dark:bg-slate-850 border hover:border-slate-400 dark:hover:border-slate-700 transition-all cursor-pointer flex flex-col justify-between space-y-3 group shadow-sm dark:shadow"
          :class="getCardBorder(verdict.status)"
        >
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <span class="font-mono text-xs font-bold text-slate-800 dark:text-white">{{ getExamCode(verdict.exam_id) }}</span>
              <span
                class="px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider"
                :class="getStatusBadgeClass(verdict.status)"
              >
                {{ formatStatus(verdict.status) }}
              </span>
            </div>

            <h4 class="text-sm font-bold text-slate-900 dark:text-white group-hover:text-emerald-500 dark:group-hover:text-emerald-400 transition-colors leading-snug">
              {{ getExamTitle(verdict.exam_id) }}
            </h4>

            <!-- Skipped criteria callout if Needs Info -->
            <div
              v-if="verdict.status === 'NEEDS_INFO' && verdict.skipped_requirements?.length"
              class="p-2 rounded-lg bg-amber-50 dark:bg-amber-500/10 border border-amber-200 dark:border-amber-500/30 text-[11px] text-amber-800 dark:text-amber-300 space-y-0.5"
            >
              <div class="font-semibold">Missing from profile:</div>
              <div class="truncate text-amber-700 dark:text-amber-200">{{ verdict.skipped_requirements[0] }}</div>
            </div>

            <!-- Reasons Snippet -->
            <div class="text-[11px] text-slate-600 dark:text-slate-400 line-clamp-2">
              {{ verdict.reasons[0] }}
            </div>
          </div>

          <div class="pt-2 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-[11px]">
            <span class="text-slate-500">{{ getExamAdmin(verdict.exam_id) }}</span>
            <span class="text-emerald-600 dark:text-emerald-400 font-semibold group-hover:translate-x-0.5 transition-transform">
              Audit Details →
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useProfileStore } from '@/stores/useProfileStore';
import { useEligibilityStore } from '@/stores/useEligibilityStore';
import { useExamMasterStore } from '@/stores/useExamMasterStore';
import { useAuthStore } from '@/stores/useAuthStore';
import type { EligibilityVerdict } from '@/types/profile';

const router = useRouter();
const profileStore = useProfileStore();
const eligibilityStore = useEligibilityStore();
const examStore = useExamMasterStore();
const authStore = useAuthStore();

const activeTab = ref<'profile' | 'summary'>('profile');
const statusFilter = ref<string>('ALL');
const isSavingProfile = ref(false);
const saveMessage = ref<string | null>(null);

const profile = profileStore.profile;

async function saveProfile() {
  isSavingProfile.value = true;
  saveMessage.value = null;
  try {
    await profileStore.saveProgress();
    saveMessage.value = 'Profile saved successfully!';
  } catch (err: any) {
    saveMessage.value = 'Profile saved locally.';
  } finally {
    isSavingProfile.value = false;
    setTimeout(() => {
      saveMessage.value = null;
    }, 4000);
  }
}

onMounted(async () => {
  await examStore.loadExams();
  await profileStore.loadInitialProfile();
  await eligibilityStore.evaluateAllExams(profileStore.profile);
});

// Re-evaluate eligibility when profile changes
watch(
  () => profileStore.profile,
  async () => {
    await eligibilityStore.evaluateAllExams(profileStore.profile);
  },
  { deep: true }
);

function toggleLanguage(lang: string) {
  if (!profile.fluent_languages) {
    profile.fluent_languages = [];
  }
  const idx = profile.fluent_languages.indexOf(lang);
  if (idx >= 0) {
    profile.fluent_languages.splice(idx, 1);
  } else {
    profile.fluent_languages.push(lang);
  }
}

function getExamCode(examId: string): string {
  return examStore.examsMap[examId]?.short_code || examId;
}

function getExamTitle(examId: string): string {
  return examStore.examsMap[examId]?.title || examId;
}

function getExamAdmin(examId: string): string {
  return examStore.examsMap[examId]?.administering_body || 'Official Commission';
}

const summaryVerdicts = computed<EligibilityVerdict[]>(() => {
  let list = eligibilityStore.verdictList;
  if (statusFilter.value !== 'ALL') {
    list = list.filter((v) => v.status === statusFilter.value);
  }
  return list;
});

function formatStatus(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'Eligible';
    case 'NEEDS_INFO':
      return 'Missing Info';
    case 'INELIGIBLE':
      return 'Ineligible';
    default:
      return status;
  }
}

function getStatusBadgeClass(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'bg-emerald-500/15 text-emerald-600 dark:text-emerald-300 border-emerald-500/40';
    case 'NEEDS_INFO':
      return 'bg-amber-500/15 text-amber-600 dark:text-amber-300 border-amber-500/40';
    case 'INELIGIBLE':
      return 'bg-rose-500/15 text-rose-600 dark:text-rose-300 border-rose-500/40';
    default:
      return 'bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border-slate-300 dark:border-slate-700';
  }
}

function getCardBorder(status: string): string {
  switch (status) {
    case 'ELIGIBLE':
      return 'border-emerald-300 dark:border-emerald-500/30 hover:border-emerald-500/60';
    case 'NEEDS_INFO':
      return 'border-amber-300 dark:border-amber-500/30 hover:border-amber-500/60';
    case 'INELIGIBLE':
      return 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700';
    default:
      return 'border-slate-200 dark:border-slate-800';
  }
}
</script>
