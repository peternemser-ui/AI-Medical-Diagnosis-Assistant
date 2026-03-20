<template>
  <div class="doctor-avatar-container flex flex-col items-center">
    <!-- Avatar circle -->
    <div
      class="relative rounded-full overflow-hidden border-4 transition-all duration-500"
      :class="[sizeClasses, speaking ? 'border-blue-400 shadow-lg shadow-blue-500/30' : 'border-slate-600']"
    >
      <!-- ══ PHOTO MODE ══ -->
      <div v-if="avatar.avatarStyle === 'photo' && avatar.photoUrl" class="w-full h-full relative">
        <img :src="avatar.photoUrl" alt="Doctor avatar" class="w-full h-full object-cover" />
        <!-- Speaking overlay pulse -->
        <div v-if="speaking" class="absolute inset-0 bg-blue-400/10 animate-pulse"></div>
      </div>

      <!-- ══ REALISTIC MODE ══ -->
      <svg v-else-if="avatar.avatarStyle === 'realistic'" ref="svgRef" viewBox="0 0 200 200" class="w-full h-full">
        <defs>
          <!-- Skin gradient for realistic shading -->
          <radialGradient id="skinGrad" cx="45%" cy="40%" r="55%">
            <stop offset="0%" :stop-color="skinHighlight" />
            <stop offset="70%" :stop-color="avatar.skinTone" />
            <stop offset="100%" :stop-color="skinShadow" />
          </radialGradient>
          <radialGradient id="neckGrad" cx="50%" cy="0%" r="80%">
            <stop offset="0%" :stop-color="avatar.skinTone" />
            <stop offset="100%" :stop-color="skinShadow" />
          </radialGradient>
          <!-- Eye iris gradient -->
          <radialGradient id="irisGradL" cx="40%" cy="35%" r="55%">
            <stop offset="0%" :stop-color="irisHighlight" />
            <stop offset="60%" :stop-color="avatar.eyeColor" />
            <stop offset="100%" :stop-color="irisDark" />
          </radialGradient>
          <radialGradient id="irisGradR" cx="40%" cy="35%" r="55%">
            <stop offset="0%" :stop-color="irisHighlight" />
            <stop offset="60%" :stop-color="avatar.eyeColor" />
            <stop offset="100%" :stop-color="irisDark" />
          </radialGradient>
          <!-- Lip gradient -->
          <linearGradient id="lipGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" :stop-color="avatar.lipColor" />
            <stop offset="100%" :stop-color="lipDark" />
          </linearGradient>
          <!-- Hair gradient -->
          <linearGradient id="hairGrad" x1="0" y1="0" x2="0.3" y2="1">
            <stop offset="0%" :stop-color="hairHighlight" />
            <stop offset="50%" :stop-color="avatar.hairColor" />
            <stop offset="100%" :stop-color="hairDark" />
          </linearGradient>
          <!-- Coat gradient -->
          <linearGradient id="coatGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" :stop-color="avatar.coatColor" />
            <stop offset="100%" :stop-color="coatShadow" />
          </linearGradient>
          <!-- Nose shadow -->
          <linearGradient id="noseShadow" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#00000000" />
            <stop offset="100%" stop-color="#00000018" />
          </linearGradient>
          <!-- Eye white gradient -->
          <radialGradient id="eyeWhiteL" cx="50%" cy="45%" r="55%">
            <stop offset="0%" stop-color="#ffffff" />
            <stop offset="100%" stop-color="#e8e4e0" />
          </radialGradient>
          <!-- Cheek blush -->
          <radialGradient id="blushL" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#e8a090" stop-opacity="0.25" />
            <stop offset="100%" stop-color="#e8a090" stop-opacity="0" />
          </radialGradient>
          <!-- Ambient shadow under chin -->
          <linearGradient id="chinShadow" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#00000000" />
            <stop offset="100%" stop-color="#00000025" />
          </linearGradient>
        </defs>

        <!-- Background -->
        <circle cx="100" cy="100" r="100" :fill="avatar.bgColor" />
        <!-- Subtle vignette -->
        <circle cx="100" cy="100" r="100" fill="url(#chinShadow)" opacity="0.3" />

        <!-- Body group — breathing -->
        <g :style="{ transform: `translate(0, ${bodyBob}px) scale(${1 + breathe}, ${1 + breathe})`, transformOrigin: '100px 170px' }">
        <!-- Body / Coat with gradient -->
        <path d="M35,200 Q35,145 65,135 Q80,130 100,128 Q120,130 135,135 Q165,145 165,200" fill="url(#coatGrad)" />
        <!-- Coat lapels with shadow -->
        <path d="M78,142 L100,168 L88,200 L68,200 Z" fill="white" opacity="0.9" />
        <path d="M122,142 L100,168 L112,200 L132,200 Z" fill="white" opacity="0.9" />
        <!-- Lapel shadow line -->
        <path d="M78,142 L100,168" fill="none" stroke="#00000015" stroke-width="1" />
        <path d="M122,142 L100,168" fill="none" stroke="#00000015" stroke-width="1" />
        <!-- Collar / shirt -->
        <path d="M85,132 L100,148 L115,132" fill="none" stroke="#ddd" stroke-width="2" />

        <!-- Stethoscope -->
        <path d="M82,152 Q70,168 74,188" fill="none" :stroke="avatar.accessoryColor" stroke-width="2.5" stroke-linecap="round" />
        <circle cx="74" cy="190" r="4.5" :fill="avatar.accessoryColor" />
        <circle cx="74" cy="190" r="2.5" fill="#555" />

        </g><!-- /Body group -->

        <!-- Neck with shading -->
        <path d="M86,118 Q86,132 88,135 L112,135 Q114,132 114,118" fill="url(#neckGrad)" />
        <!-- Neck shadow under jaw -->
        <ellipse cx="100" cy="120" rx="16" ry="4" fill="#00000012" />

        <!-- Head group — tilt + bob -->
        <g :style="{ transform: `translate(0, ${bodyBob * 0.7}px) rotate(${headTilt}deg)`, transformOrigin: '100px 90px' }">
        <!-- Head with realistic gradient -->
        <ellipse cx="100" cy="82" rx="40" ry="44" fill="url(#skinGrad)" />
        <!-- Jawline definition -->
        <path d="M62,90 Q65,120 100,125 Q135,120 138,90" fill="none" stroke="#00000008" stroke-width="1.5" />

        <!-- Ear left -->
        <ellipse cx="60" cy="85" rx="5" ry="9" :fill="avatar.skinTone" />
        <ellipse cx="60" cy="85" rx="3" ry="6" :fill="skinShadow" opacity="0.3" />
        <!-- Ear right -->
        <ellipse cx="140" cy="85" rx="5" ry="9" :fill="avatar.skinTone" />
        <ellipse cx="140" cy="85" rx="3" ry="6" :fill="skinShadow" opacity="0.3" />

        <!-- Hair with gradient and volume -->
        <g v-if="avatar.hairStyle === 'short'">
          <ellipse cx="100" cy="56" rx="40" ry="24" fill="url(#hairGrad)" />
          <!-- Side hair -->
          <path d="M60,70 Q58,55 65,45 Q75,38 100,36 Q125,38 135,45 Q142,55 140,70" fill="url(#hairGrad)" />
          <!-- Hair texture lines -->
          <path d="M75,42 Q85,38 100,37" fill="none" :stroke="hairHighlight" stroke-width="0.8" opacity="0.4" />
          <path d="M110,38 Q125,40 132,48" fill="none" :stroke="hairHighlight" stroke-width="0.8" opacity="0.4" />
        </g>
        <g v-if="avatar.hairStyle === 'long'">
          <path d="M58,88 Q55,35 100,38 Q145,35 142,88 L140,65 Q135,42 100,45 Q65,42 60,65 Z" fill="url(#hairGrad)" />
          <!-- Long strands framing face -->
          <path d="M60,85 Q58,105 62,120" fill="none" :stroke="avatar.hairColor" stroke-width="4" stroke-linecap="round" opacity="0.85" />
          <path d="M140,85 Q142,105 138,120" fill="none" :stroke="avatar.hairColor" stroke-width="4" stroke-linecap="round" opacity="0.85" />
          <!-- Highlight strands -->
          <path d="M80,42 Q90,38 100,40" fill="none" :stroke="hairHighlight" stroke-width="1" opacity="0.35" />
        </g>
        <g v-if="avatar.hairStyle === 'curly'">
          <path d="M56,82 Q50,38 78,35 Q72,26 100,32 Q128,26 122,35 Q150,38 144,82 L142,62 Q138,40 100,43 Q62,40 58,62 Z" fill="url(#hairGrad)" />
          <!-- Curl details -->
          <circle cx="62" cy="55" r="5" :fill="avatar.hairColor" opacity="0.6" />
          <circle cx="72" cy="42" r="4" :fill="avatar.hairColor" opacity="0.5" />
          <circle cx="138" cy="55" r="5" :fill="avatar.hairColor" opacity="0.6" />
          <circle cx="128" cy="42" r="4" :fill="avatar.hairColor" opacity="0.5" />
          <circle cx="100" cy="34" r="4.5" :fill="avatar.hairColor" opacity="0.5" />
        </g>
        <g v-if="avatar.hairStyle === 'bald'">
          <path d="M60,75 Q60,48 100,45 Q140,48 140,75" :fill="avatar.skinTone" />
          <!-- Subtle shine on bald head -->
          <ellipse cx="90" cy="52" rx="15" ry="8" fill="white" opacity="0.08" />
        </g>
        <g v-if="avatar.hairStyle === 'ponytail'">
          <path d="M58,88 Q55,35 100,38 Q145,35 142,88 L140,65 Q135,42 100,45 Q65,42 60,65 Z" fill="url(#hairGrad)" />
          <path d="M132,52 Q158,55 154,100 Q152,115 142,108" fill="url(#hairGrad)" />
          <!-- Hair tie -->
          <ellipse cx="136" cy="58" rx="3" ry="4" fill="#333" opacity="0.5" />
          <path d="M80,42 Q90,38 100,40" fill="none" :stroke="hairHighlight" stroke-width="1" opacity="0.35" />
        </g>

        <!-- Eyebrows - more natural shape -->
        <g :class="speaking ? 'avatar-brows' : 'avatar-brows-idle'">
          <path d="M70,71 Q76,65 83,67 Q88,68 92,71" fill="none" :stroke="avatar.hairColor" stroke-width="2" stroke-linecap="round" opacity="0.85" />
          <path d="M108,71 Q112,68 117,67 Q124,65 130,71" fill="none" :stroke="avatar.hairColor" stroke-width="2" stroke-linecap="round" opacity="0.85" />
        </g>

        <!-- Eyes - realistic with gradient irises, always blink -->
        <g :class="speaking ? 'avatar-blink' : 'avatar-idle-blink'">
          <!-- Eye sockets (subtle shadow) -->
          <ellipse cx="82" cy="81" rx="10" ry="7" fill="#00000008" />
          <ellipse cx="118" cy="81" rx="10" ry="7" fill="#00000008" />
          <!-- Upper eyelid crease -->
          <path d="M72,76 Q82,72 92,76" fill="none" stroke="#00000018" stroke-width="1" />
          <path d="M108,76 Q118,72 128,76" fill="none" stroke="#00000018" stroke-width="1" />
          <!-- Eye whites with gradient -->
          <ellipse cx="82" cy="81" rx="8" ry="6.5" fill="url(#eyeWhiteL)" />
          <ellipse cx="118" cy="81" rx="8" ry="6.5" fill="url(#eyeWhiteL)" />
          <!-- Iris with gradient (follows mouse) -->
          <circle :cx="82 + pupilOffsetX" :cy="81.5 + pupilOffsetY" r="4.5" fill="url(#irisGradL)" class="transition-[cx,cy] duration-75" />
          <circle :cx="118 + pupilOffsetX" :cy="81.5 + pupilOffsetY" r="4.5" fill="url(#irisGradR)" class="transition-[cx,cy] duration-75" />
          <!-- Pupil -->
          <circle :cx="82 + pupilOffsetX" :cy="81.5 + pupilOffsetY" r="2" fill="#0a0a0a" class="transition-[cx,cy] duration-75" />
          <circle :cx="118 + pupilOffsetX" :cy="81.5 + pupilOffsetY" r="2" fill="#0a0a0a" class="transition-[cx,cy] duration-75" />
          <!-- Specular highlight -->
          <circle :cx="84 + pupilOffsetX * 0.5" :cy="79.5 + pupilOffsetY * 0.5" r="1.8" fill="white" opacity="0.9" class="transition-[cx,cy] duration-75" />
          <circle :cx="120 + pupilOffsetX * 0.5" :cy="79.5 + pupilOffsetY * 0.5" r="1.8" fill="white" opacity="0.9" class="transition-[cx,cy] duration-75" />
          <!-- Secondary highlight -->
          <circle :cx="80.5 + pupilOffsetX * 0.3" :cy="83 + pupilOffsetY * 0.3" r="0.8" fill="white" opacity="0.5" class="transition-[cx,cy] duration-75" />
          <circle :cx="116.5 + pupilOffsetX * 0.3" :cy="83 + pupilOffsetY * 0.3" r="0.8" fill="white" opacity="0.5" class="transition-[cx,cy] duration-75" />
          <!-- Upper eyelid line -->
          <path d="M74,79 Q82,74 90,79" fill="none" stroke="#00000030" stroke-width="1.2" stroke-linecap="round" />
          <path d="M110,79 Q118,74 126,79" fill="none" stroke="#00000030" stroke-width="1.2" stroke-linecap="round" />
          <!-- Lower eyelid hint -->
          <path d="M75,84 Q82,87 89,84" fill="none" stroke="#00000010" stroke-width="0.8" />
          <path d="M111,84 Q118,87 125,84" fill="none" stroke="#00000010" stroke-width="0.8" />
          <!-- Eyelashes (subtle) -->
          <path d="M74,79 L72,77" fill="none" stroke="#00000025" stroke-width="0.8" stroke-linecap="round" />
          <path d="M90,79 L92,77" fill="none" stroke="#00000025" stroke-width="0.8" stroke-linecap="round" />
          <path d="M110,79 L108,77" fill="none" stroke="#00000025" stroke-width="0.8" stroke-linecap="round" />
          <path d="M126,79 L128,77" fill="none" stroke="#00000025" stroke-width="0.8" stroke-linecap="round" />
        </g>

        <!-- Nose - more defined -->
        <path d="M100,78 L98,92 Q95,97 92,96" fill="none" stroke="#00000018" stroke-width="1.2" stroke-linecap="round" />
        <path d="M98,92 Q100,98 102,92" fill="none" stroke="#00000020" stroke-width="1.5" stroke-linecap="round" />
        <!-- Nose shadow -->
        <ellipse cx="96" cy="95" rx="3" ry="2" fill="#00000008" />
        <!-- Nostril hints -->
        <ellipse cx="95" cy="95" rx="2" ry="1.2" fill="#00000012" />
        <ellipse cx="105" cy="95" rx="2" ry="1.2" fill="#00000012" />

        <!-- Cheek blush -->
        <ellipse cx="70" cy="93" rx="10" ry="7" fill="url(#blushL)" />
        <ellipse cx="130" cy="93" rx="10" ry="7" fill="url(#blushL)" />

        <!-- MOUTH — realistic -->
        <g class="avatar-mouth">
          <!-- Resting mouth -->
          <g v-if="!speaking">
            <!-- Upper lip -->
            <path d="M87,103 Q93,100 100,101.5 Q107,100 113,103" fill="url(#lipGrad)" />
            <!-- Cupid's bow -->
            <path d="M93,101.5 Q97,99 100,100 Q103,99 107,101.5" fill="url(#lipGrad)" />
            <!-- Lower lip -->
            <path d="M87,103 Q100,111 113,103" fill="url(#lipGrad)" />
            <!-- Lip line -->
            <path d="M87,103 Q100,105 113,103" fill="none" :stroke="lipDark" stroke-width="0.8" opacity="0.5" />
            <!-- Lip highlight -->
            <ellipse cx="100" cy="106" rx="6" ry="2" fill="white" opacity="0.08" />
            <!-- Subtle smile crease -->
            <path d="M84,104 Q85,106 87,103" fill="none" stroke="#00000012" stroke-width="0.8" />
            <path d="M116,104 Q115,106 113,103" fill="none" stroke="#00000012" stroke-width="0.8" />
          </g>

          <!-- Speaking mouth shapes -->
          <g v-if="speaking">
            <!-- Shape A: Open wide "ah" -->
            <ellipse class="mouth-shape mouth-a" cx="100" cy="106" rx="11" ry="8" fill="#1a0505" />
            <path class="mouth-shape mouth-a" d="M89,103 Q94,99 100,100.5 Q106,99 111,103" fill="url(#lipGrad)" />
            <path class="mouth-shape mouth-a" d="M89,110 Q100,116 111,110" fill="url(#lipGrad)" />
            <rect class="mouth-shape mouth-a" x="94" y="101" width="12" height="3" rx="1" fill="white" opacity="0.75" />
            <ellipse class="mouth-shape mouth-a" cx="100" cy="111" rx="5" ry="2.5" fill="#c45050" opacity="0.5" />

            <!-- Shape B: Medium "oh" -->
            <ellipse class="mouth-shape mouth-b" cx="100" cy="105.5" rx="7" ry="6" fill="#1a0505" />
            <path class="mouth-shape mouth-b" d="M93,103 Q97,101 100,102 Q103,101 107,103" fill="url(#lipGrad)" />
            <path class="mouth-shape mouth-b" d="M93,108 Q100,113 107,108" fill="url(#lipGrad)" />
            <rect class="mouth-shape mouth-b" x="96" y="102" width="8" height="2" rx="1" fill="white" opacity="0.65" />

            <!-- Shape C: Wide "ee" -->
            <ellipse class="mouth-shape mouth-c" cx="100" cy="104.5" rx="11" ry="3" fill="#1a0505" />
            <path class="mouth-shape mouth-c" d="M89,103.5 Q100,101 111,103.5" fill="url(#lipGrad)" />
            <path class="mouth-shape mouth-c" d="M89,105.5 Q100,109 111,105.5" fill="url(#lipGrad)" />

            <!-- Shape D: Small "mm" -->
            <ellipse class="mouth-shape mouth-d" cx="100" cy="104.5" rx="5" ry="3.5" fill="#1a0505" />
            <path class="mouth-shape mouth-d" d="M95,103 Q100,101.5 105,103" fill="url(#lipGrad)" />
            <path class="mouth-shape mouth-d" d="M95,106 Q100,109 105,106" fill="url(#lipGrad)" />
          </g>
        </g>

        <!-- Glasses (optional) - more realistic -->
        <g v-if="avatar.glasses">
          <rect x="69" y="73" width="26" height="18" rx="4" fill="none" :stroke="avatar.accessoryColor" stroke-width="1.8" />
          <rect x="105" y="73" width="26" height="18" rx="4" fill="none" :stroke="avatar.accessoryColor" stroke-width="1.8" />
          <path d="M95,82 L105,82" fill="none" :stroke="avatar.accessoryColor" stroke-width="1.5" />
          <path d="M69,80 L60,78" fill="none" :stroke="avatar.accessoryColor" stroke-width="1.5" />
          <path d="M131,80 L140,78" fill="none" :stroke="avatar.accessoryColor" stroke-width="1.5" />
          <!-- Lens reflection -->
          <ellipse cx="78" cy="78" rx="4" ry="3" fill="white" opacity="0.06" />
          <ellipse cx="114" cy="78" rx="4" ry="3" fill="white" opacity="0.06" />
        </g>
        </g><!-- /Head group -->

        <!-- Waving arm (realistic) -->
        <g v-if="waving" class="avatar-wave" style="transform-origin: 148px 140px">
          <path d="M135,142 Q148,128 152,110 L162,108 Q160,130 145,145 Z" fill="url(#coatGrad)" />
          <path d="M155,110 Q162,90 155,75" fill="none" :stroke="avatar.skinTone" stroke-width="10" stroke-linecap="round" />
          <circle cx="155" cy="72" r="7" :fill="avatar.skinTone" />
          <path d="M150,68 L147,60" fill="none" :stroke="avatar.skinTone" stroke-width="2.5" stroke-linecap="round" />
          <path d="M153,66 L151,57" fill="none" :stroke="avatar.skinTone" stroke-width="2.5" stroke-linecap="round" />
          <path d="M157,66 L157,57" fill="none" :stroke="avatar.skinTone" stroke-width="2.5" stroke-linecap="round" />
          <path d="M160,68 L163,60" fill="none" :stroke="avatar.skinTone" stroke-width="2.5" stroke-linecap="round" />
          <ellipse cx="156" cy="108" rx="7" ry="3" fill="url(#coatGrad)" />
        </g>

        <!-- ID Badge - more realistic -->
        <rect x="116" y="154" width="18" height="25" rx="2" fill="white" opacity="0.92" />
        <rect x="116" y="154" width="18" height="8" rx="2" :fill="avatar.accessoryColor" opacity="0.15" />
        <circle cx="125" cy="162" r="3.5" :fill="avatar.skinTone" opacity="0.6" />
        <rect x="119" y="168" width="12" height="1.5" rx="0.5" fill="#ccc" />
        <rect x="120" y="171" width="10" height="1" rx="0.5" fill="#ddd" />
        <!-- Badge clip -->
        <rect x="122" y="151" width="6" height="4" rx="1" fill="#999" />
      </svg>

      <!-- ══ ILLUSTRATED MODE (original) ══ -->
      <svg v-else ref="svgRef" viewBox="0 0 200 200" class="w-full h-full">
        <!-- Background circle -->
        <circle cx="100" cy="100" r="100" :fill="avatar.bgColor" />

        <!-- Body group — breathing animation -->
        <g :style="{ transform: `translate(0, ${bodyBob}px) scale(${1 + breathe}, ${1 + breathe})`, transformOrigin: '100px 170px' }">
        <!-- Body / Coat -->
        <path d="M40,200 Q40,140 100,130 Q160,140 160,200" :fill="avatar.coatColor" />
        <!-- Coat lapels -->
        <path d="M80,145 L100,170 L90,200 L70,200 Z" fill="white" opacity="0.9" />
        <path d="M120,145 L100,170 L110,200 L130,200 Z" fill="white" opacity="0.9" />

        <!-- Stethoscope -->
        <path d="M85,155 Q75,170 78,185" fill="none" :stroke="avatar.accessoryColor" stroke-width="3" stroke-linecap="round" />
        <circle cx="78" cy="188" r="5" :fill="avatar.accessoryColor" />
        </g>

        <!-- Neck -->
        <rect x="88" y="115" width="24" height="20" :fill="avatar.skinTone" rx="4" />

        <!-- Head group — tilt + bob -->
        <g :style="{ transform: `translate(0, ${bodyBob * 0.7}px) rotate(${headTilt}deg)`, transformOrigin: '100px 95px' }">
        <!-- Head -->
        <ellipse cx="100" cy="85" rx="38" ry="42" :fill="avatar.skinTone" />

        <!-- Hair -->
        <ellipse v-if="avatar.hairStyle === 'short'" cx="100" cy="60" rx="38" ry="22" :fill="avatar.hairColor" />
        <path v-if="avatar.hairStyle === 'long'" d="M62,85 Q62,35 100,40 Q138,35 138,85 L135,70 Q130,45 100,48 Q70,45 65,70 Z" :fill="avatar.hairColor" />
        <path v-if="avatar.hairStyle === 'curly'" d="M60,80 Q55,40 80,38 Q75,30 100,35 Q125,30 120,38 Q145,40 140,80 L138,65 Q135,42 100,45 Q65,42 62,65 Z" :fill="avatar.hairColor" />
        <path v-if="avatar.hairStyle === 'bald'" d="M62,75 Q62,50 100,48 Q138,50 138,75" :fill="avatar.skinTone" />
        <path v-if="avatar.hairStyle === 'ponytail'" d="M62,85 Q62,35 100,40 Q138,35 138,85 L135,70 Q130,45 100,48 Q70,45 65,70 Z" :fill="avatar.hairColor" />
        <path v-if="avatar.hairStyle === 'ponytail'" d="M130,55 Q155,60 150,100 Q148,110 140,105" :fill="avatar.hairColor" />

        <!-- Eyes - always blink, faster when speaking, pupils follow cursor -->
        <g :class="speaking ? 'avatar-blink' : 'avatar-idle-blink'">
          <!-- Eye whites -->
          <ellipse cx="82" cy="82" rx="6" ry="7" fill="white" />
          <ellipse cx="118" cy="82" rx="6" ry="7" fill="white" />
          <!-- Irises + pupils (follow mouse) -->
          <circle :cx="83 + pupilOffsetX" :cy="83 + pupilOffsetY" r="3.5" :fill="avatar.eyeColor" class="transition-[cx,cy] duration-75" />
          <circle :cx="119 + pupilOffsetX" :cy="83 + pupilOffsetY" r="3.5" :fill="avatar.eyeColor" class="transition-[cx,cy] duration-75" />
          <!-- Specular highlights (follow with pupils) -->
          <circle :cx="84 + pupilOffsetX * 0.6" :cy="82 + pupilOffsetY * 0.6" r="1.5" fill="white" class="transition-[cx,cy] duration-75" />
          <circle :cx="120 + pupilOffsetX * 0.6" :cy="82 + pupilOffsetY * 0.6" r="1.5" fill="white" class="transition-[cx,cy] duration-75" />
        </g>

        <!-- Eyebrows - raise slightly when speaking -->
        <g :class="speaking ? 'avatar-brows' : 'avatar-brows-idle'">
          <path d="M73,73 Q82,68 91,73" fill="none" :stroke="avatar.hairColor" stroke-width="2.5" stroke-linecap="round" />
          <path d="M109,73 Q118,68 127,73" fill="none" :stroke="avatar.hairColor" stroke-width="2.5" stroke-linecap="round" />
        </g>

        <!-- Nose -->
        <path d="M97,88 Q100,96 103,88" fill="none" stroke="#00000020" stroke-width="2" />

        <!-- MOUTH — Animated lip sync -->
        <g class="avatar-mouth">
          <!-- Resting mouth (closed smile) -->
          <path
            v-if="!speaking"
            d="M88,104 Q100,112 112,104"
            fill="none" :stroke="avatar.lipColor" stroke-width="2.5" stroke-linecap="round"
          />

          <!-- Speaking mouth — multiple shapes cycling via CSS animation -->
          <g v-if="speaking">
            <ellipse class="mouth-shape mouth-a" cx="100" cy="106" rx="10" ry="8" :fill="'#2a0a0a'" />
            <ellipse class="mouth-shape mouth-a" cx="100" cy="106" rx="10" ry="8" fill="none" :stroke="avatar.lipColor" stroke-width="2" />
            <path class="mouth-shape mouth-a" d="M90,103 Q95,100 100,101 Q105,100 110,103" :fill="avatar.lipColor" />
            <ellipse class="mouth-shape mouth-b" cx="100" cy="106" rx="7" ry="6" :fill="'#2a0a0a'" />
            <ellipse class="mouth-shape mouth-b" cx="100" cy="106" rx="7" ry="6" fill="none" :stroke="avatar.lipColor" stroke-width="2" />
            <path class="mouth-shape mouth-b" d="M93,104 Q97,102 100,103 Q103,102 107,104" :fill="avatar.lipColor" />
            <ellipse class="mouth-shape mouth-c" cx="100" cy="105" rx="10" ry="3" :fill="'#2a0a0a'" />
            <ellipse class="mouth-shape mouth-c" cx="100" cy="105" rx="10" ry="3" fill="none" :stroke="avatar.lipColor" stroke-width="2" />
            <path class="mouth-shape mouth-c" d="M90,104 Q100,102 110,104" :fill="avatar.lipColor" />
            <ellipse class="mouth-shape mouth-d" cx="100" cy="105" rx="5" ry="4" :fill="'#2a0a0a'" />
            <ellipse class="mouth-shape mouth-d" cx="100" cy="105" rx="5" ry="4" fill="none" :stroke="avatar.lipColor" stroke-width="2" />
            <path class="mouth-shape mouth-d" d="M95,104 Q100,102 105,104" :fill="avatar.lipColor" />
            <rect class="mouth-shape mouth-a" x="94" y="102" width="12" height="3" rx="1" fill="white" opacity="0.8" />
            <rect class="mouth-shape mouth-b" x="96" y="103" width="8" height="2" rx="1" fill="white" opacity="0.7" />
            <ellipse class="mouth-shape mouth-a" cx="100" cy="110" rx="5" ry="2.5" fill="#c45050" opacity="0.6" />
          </g>
        </g>

        <!-- Glasses (optional) -->
        <g v-if="avatar.glasses">
          <circle cx="82" cy="82" r="12" fill="none" :stroke="avatar.accessoryColor" stroke-width="2" />
          <circle cx="118" cy="82" r="12" fill="none" :stroke="avatar.accessoryColor" stroke-width="2" />
          <path d="M94,82 L106,82" fill="none" :stroke="avatar.accessoryColor" stroke-width="2" />
          <path d="M70,80 L62,78" fill="none" :stroke="avatar.accessoryColor" stroke-width="2" />
          <path d="M130,80 L138,78" fill="none" :stroke="avatar.accessoryColor" stroke-width="2" />
        </g>
        </g><!-- /Head group -->

        <!-- Waving arm -->
        <g v-if="waving" class="avatar-wave" style="transform-origin: 148px 140px">
          <!-- Upper arm -->
          <path d="M140,140 Q155,125 158,105" :fill="avatar.coatColor" stroke="none" />
          <path d="M135,142 Q148,128 152,110 L162,108 Q160,130 145,145 Z" :fill="avatar.coatColor" />
          <!-- Forearm + hand -->
          <path d="M155,110 Q162,90 155,75" fill="none" :stroke="avatar.skinTone" stroke-width="10" stroke-linecap="round" />
          <!-- Hand -->
          <circle cx="155" cy="72" r="7" :fill="avatar.skinTone" />
          <!-- Fingers spread -->
          <path d="M150,68 L147,60" fill="none" :stroke="avatar.skinTone" stroke-width="2.5" stroke-linecap="round" />
          <path d="M153,66 L151,57" fill="none" :stroke="avatar.skinTone" stroke-width="2.5" stroke-linecap="round" />
          <path d="M157,66 L157,57" fill="none" :stroke="avatar.skinTone" stroke-width="2.5" stroke-linecap="round" />
          <path d="M160,68 L163,60" fill="none" :stroke="avatar.skinTone" stroke-width="2.5" stroke-linecap="round" />
          <!-- Sleeve cuff -->
          <ellipse cx="156" cy="108" rx="7" ry="3" :fill="avatar.coatColor" />
        </g>

        <!-- ID Badge -->
        <rect x="115" y="155" width="18" height="24" rx="2" fill="white" opacity="0.9" />
        <rect x="118" y="158" width="12" height="3" rx="1" :fill="avatar.accessoryColor" opacity="0.6" />
        <rect x="118" y="163" width="12" height="1.5" rx="0.5" fill="#ccc" />
        <rect x="118" y="166" width="8" height="1.5" rx="0.5" fill="#ccc" />
      </svg>

      <!-- Speaking indicator ring -->
      <div v-if="speaking" class="absolute inset-0 rounded-full border-4 border-blue-400/40 animate-ping pointer-events-none"></div>
    </div>

    <!-- Name plate -->
    <div v-if="showName" class="mt-2 text-center">
      <div class="text-sm font-semibold text-white">{{ avatar.name }}</div>
      <div class="text-[10px] text-slate-400">{{ avatar.specialty }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  avatar: { type: Object, required: true },
  speaking: { type: Boolean, default: false },
  waving: { type: Boolean, default: false },
  showName: { type: Boolean, default: true },
  size: { type: String, default: 'md' }
})

const sizeClasses = {
  sm: 'w-16 h-16',
  md: 'w-24 h-24',
  lg: 'w-36 h-36',
  xl: 'w-64 h-64 sm:w-72 sm:h-72',
  xxl: 'w-80 h-80 sm:w-96 sm:h-96',
  xxxl: 'w-[min(70vh,28rem)] h-[min(70vh,28rem)] sm:w-[min(55vh,34rem)] sm:h-[min(55vh,34rem)]',
}[props.size] || 'w-24 h-24'

// Color helpers for realistic mode
function adjustColor(hex, amount) {
  const num = parseInt((hex || '#888888').replace('#', ''), 16)
  const r = Math.min(255, Math.max(0, (num >> 16) + amount))
  const g = Math.min(255, Math.max(0, ((num >> 8) & 0xff) + amount))
  const b = Math.min(255, Math.max(0, (num & 0xff) + amount))
  return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, '0')}`
}

const skinHighlight = computed(() => adjustColor(props.avatar.skinTone, 25))
const skinShadow = computed(() => adjustColor(props.avatar.skinTone, -35))
const hairHighlight = computed(() => adjustColor(props.avatar.hairColor, 40))
const hairDark = computed(() => adjustColor(props.avatar.hairColor, -30))
const irisHighlight = computed(() => adjustColor(props.avatar.eyeColor, 50))
const irisDark = computed(() => adjustColor(props.avatar.eyeColor, -50))
const lipDark = computed(() => adjustColor(props.avatar.lipColor, -30))
const coatShadow = computed(() => adjustColor(props.avatar.coatColor, -20))

// Eye tracking
const svgRef = ref(null)
const pupilOffsetX = ref(0)
const pupilOffsetY = ref(0)
const MAX_OFFSET = 3

// Idle animation state
const headTilt = ref(0)
const bodyBob = ref(0)
const breathe = ref(0)
let idleFrame = null

function onMouseMove(e) {
  if (!svgRef.value) return
  const rect = svgRef.value.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2
  const dx = e.clientX - centerX
  const dy = e.clientY - centerY
  const dist = Math.sqrt(dx * dx + dy * dy) || 1
  const clamp = Math.min(dist, 300) / 300
  pupilOffsetX.value = (dx / dist) * clamp * MAX_OFFSET
  pupilOffsetY.value = (dy / dist) * clamp * MAX_OFFSET
}

function animateIdle(time) {
  // Head tilt side to side — noticeable sway
  headTilt.value = Math.sin(time * 0.0006) * 4 + Math.sin(time * 0.0015) * 1.5
  // Vertical bob
  bodyBob.value = Math.sin(time * 0.001) * 1.5
  // Breathing — chest/body scale pulse
  breathe.value = Math.sin(time * 0.002) * 0.008
  idleFrame = requestAnimationFrame(animateIdle)
}

onMounted(() => {
  window.addEventListener('mousemove', onMouseMove)
  idleFrame = requestAnimationFrame(animateIdle)
})
onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  if (idleFrame) cancelAnimationFrame(idleFrame)
})
</script>

<style scoped>
/* ── Mouth animation: cycle through 4 viseme shapes ── */
.mouth-shape {
  opacity: 0;
}

.mouth-a { animation: viseme-a 0.8s steps(1) infinite; }
.mouth-b { animation: viseme-b 0.8s steps(1) infinite; }
.mouth-c { animation: viseme-c 0.8s steps(1) infinite; }
.mouth-d { animation: viseme-d 0.8s steps(1) infinite; }

@keyframes viseme-a {
  0%, 100%   { opacity: 1; }
  25%        { opacity: 0; }
  50%        { opacity: 0; }
  75%        { opacity: 0; }
}
@keyframes viseme-b {
  0%         { opacity: 0; }
  25%, 50%   { opacity: 0; }
  50%        { opacity: 0; }
  75%        { opacity: 1; }
}
@keyframes viseme-c {
  0%         { opacity: 0; }
  25%        { opacity: 0; }
  50%        { opacity: 1; }
  75%        { opacity: 0; }
}
@keyframes viseme-d {
  0%         { opacity: 0; }
  25%        { opacity: 1; }
  50%        { opacity: 0; }
  75%        { opacity: 0; }
}

.mouth-a { animation-duration: 0.7s; }
.mouth-b { animation-duration: 0.9s; }
.mouth-c { animation-duration: 0.6s; }
.mouth-d { animation-duration: 0.8s; }

/* ── Eye blink — always active (idle + speaking) ── */
.avatar-blink {
  animation: blink 3.5s ease-in-out infinite;
}
.avatar-idle-blink {
  animation: blink 5s ease-in-out infinite;
}

@keyframes blink {
  0%, 93%, 100% { transform: scaleY(1); }
  95%           { transform: scaleY(0.05); }
  96%           { transform: scaleY(1); }
}

/* ── Eyebrow raise (speaking) ── */
.avatar-brows {
  animation: brow-raise 2.5s ease-in-out infinite;
}

/* ── Eyebrow idle — subtle micro-expression ── */
.avatar-brows-idle {
  animation: brow-idle 6s ease-in-out infinite;
}

@keyframes brow-raise {
  0%, 100% { transform: translateY(0); }
  30%      { transform: translateY(-2px); }
  60%      { transform: translateY(-0.5px); }
}

@keyframes brow-idle {
  0%, 100% { transform: translateY(0); }
  40%      { transform: translateY(-0.8px); }
  70%      { transform: translateY(0.3px); }
}

/* ── Waving hand ── */
.avatar-wave {
  animation: wave 1.8s ease-in-out infinite;
}

@keyframes wave {
  0%, 100% { transform: rotate(0deg); }
  15%      { transform: rotate(-15deg); }
  30%      { transform: rotate(12deg); }
  45%      { transform: rotate(-12deg); }
  60%      { transform: rotate(10deg); }
  75%      { transform: rotate(-5deg); }
  90%      { transform: rotate(3deg); }
}
</style>
