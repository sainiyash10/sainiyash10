import math

W, H = 495, 160
RX = 16


def build(total_contributions=4, total_range="Aug 16, 2026 \u2013 Present",
          current_streak=2, current_range="Sep 11 \u2013 Sep 12",
          longest_streak=2, longest_range="Sep 11 \u2013 Sep 12",
          ring_dash=198.7,
          out_path='assets/contribution.svg'):

    r = 34
    circumf = 2 * math.pi * r  # 213.63

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="cBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#1f0f38"/>
      <stop offset="100%" stop-color="#140823"/>
    </linearGradient>
    <linearGradient id="cRing" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%"   stop-color="#ff5fc4"/>
      <stop offset="100%" stop-color="#a259ff"/>
    </linearGradient>
    <!-- Flame gradient: pink at base \u2192 orange at tip -->
    <linearGradient id="flameGrad" x1="0%" y1="100%" x2="0%" y2="0%">
      <stop offset="0%"   stop-color="#ff5fc4"/>
      <stop offset="100%" stop-color="#ff8c5a"/>
    </linearGradient>
    <clipPath id="cClip">
      <rect width="{W}" height="{H}" rx="{RX}"/>
    </clipPath>
  </defs>

  <g clip-path="url(#cClip)">

    <!-- Background -->
    <rect width="{W}" height="{H}" fill="url(#cBg)"/>

    <!-- Border -->
    <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="15.5"
          fill="none" stroke="#a259ff" stroke-width="1.6"/>

    <!-- Dividers \u2014 solid border colour -->
    <line x1="165" y1="16" x2="165" y2="144" stroke="#a259ff" stroke-width="1"/>
    <line x1="330" y1="16" x2="330" y2="144" stroke="#a259ff" stroke-width="1"/>

    <!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
         LEFT PANEL  \u2014  Total Contributions
         panel centre x = 82  |  card h = 160  \u2192  content centred ~y 55\u2013115
         \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->
    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.1s" fill="freeze"/>

      <text x="82" y="78" text-anchor="middle"
            font-family="Segoe UI, Arial, sans-serif" font-size="40" font-weight="800"
            fill="#ff5fc4">{total_contributions}</text>

      <text x="82" y="120" text-anchor="middle"
            font-family="Segoe UI, Arial, sans-serif" font-size="11" font-weight="600"
            fill="#ff5fc4">Total Contributions</text>

      <!-- Date: white -->
      <text x="82" y="140" text-anchor="middle"
            font-family="Segoe UI, Arial, sans-serif" font-size="10.5"
            fill="#ffffff">{total_range}</text>
    </g>

    <!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
         CENTRE PANEL  \u2014  Current Streak
         Ring centre: (247, 71)   radius: 38   circumference: 238.76
         Ring top absolute y = 71 \u2013 38 = 33
         \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->

    <!-- Ghost track ring -->
    <circle cx="247" cy="64" r="{r}"
            fill="none" stroke="rgba(162,89,255,0.2)" stroke-width="6"/>

    <!-- Animated gradient arc  (start at 12-o'clock = rotate \u201390)
         leaves ~16 px gap at top for the flame -->
    <circle cx="247" cy="64" r="{r}"
            fill="none" stroke="url(#cRing)" stroke-width="6"
            stroke-linecap="round"
            stroke-dasharray="0 {circumf:.2f}"
            transform="rotate(-90 247 64)">
      <animate attributeName="stroke-dasharray"
               from="0 {circumf:.2f}" to="{ring_dash} {circumf:.2f}"
               dur="1.3s" begin="0.25s" fill="freeze"
               calcMode="spline" keySplines="0.2 0.6 0.25 1"/>
    </circle>

    <!-- \u2500\u2500 SVG Flame icon \u2014 exact path from github-readme-streak-stats \u2500\u2500
         Positioned centred on the ring's 12-o'clock point.
         Original viewBox bounding box: x=-12 to 15, y=-0.5 to 23.5
         Centre of that box: (1.5, 11.5). We translate so that centre sits at ring top. -->
    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.1s" fill="freeze"/>
      <!-- translate(247, 33): ring top. shift left by 1.5 (path centre-x), up by ~12 so flame base sits on ring -->
      <g transform="translate(245.5, 18)">
        <path d='M 1.5 0.67 C 1.5 0.67 2.24 3.32 2.24 5.47 C 2.24 7.53 0.89 9.2 -1.17 9.2
                 C -3.23 9.2 -4.79 7.53 -4.79 5.47 L -4.76 5.11
                 C -6.78 7.51 -8 10.62 -8 13.99 C -8 18.41 -4.42 22 0 22
                 C 4.42 22 8 18.41 8 13.99 C 8 8.6 5.41 3.79 1.5 0.67 Z
                 M -0.29 19 C -2.07 19 -3.51 17.6 -3.51 15.86
                 C -3.51 14.24 -2.46 13.1 -0.7 12.74 C 1.07 12.38 2.9 11.53 3.92 10.16
                 C 4.31 11.45 4.51 12.81 4.51 14.2 C 4.51 16.85 2.36 19 -0.29 19 Z'
              fill='#ff5fc4'/>
      </g>
    </g>

    <!-- Streak number \"{current_streak}\" \u2014 yellow, centred inside ring -->
    <text x="247" y="75" text-anchor="middle"
          font-family="Segoe UI, Arial, sans-serif" font-size="32" font-weight="800"
          fill="#f9e84a" opacity="0">{current_streak}
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.1s" fill="freeze"/>
    </text>

    <!-- "Current Streak" label -->
    <text x="247" y="120" text-anchor="middle"
          font-family="Segoe UI, Arial, sans-serif" font-size="11" font-weight="700"
          fill="#ff5fc4" opacity="0">Current Streak
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.1s" fill="freeze"/>
    </text>

    <!-- Centre date \u2014 white -->
    <text x="247" y="140" text-anchor="middle"
          font-family="Segoe UI, Arial, sans-serif" font-size="10.5"
          fill="#ffffff" opacity="0">{current_range}
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="1.1s" fill="freeze"/>
    </text>

    <!-- \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550
         RIGHT PANEL  \u2014  Longest Streak
         panel centre x = 412
         \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550 -->
    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.1s" fill="freeze"/>

      <text x="412" y="78" text-anchor="middle"
            font-family="Segoe UI, Arial, sans-serif" font-size="40" font-weight="800"
            fill="#ff5fc4">{longest_streak}</text>

      <text x="412" y="120" text-anchor="middle"
            font-family="Segoe UI, Arial, sans-serif" font-size="11" font-weight="600"
            fill="#ff5fc4">Longest Streak</text>

      <!-- Date: white -->
      <text x="412" y="140" text-anchor="middle"
            font-family="Segoe UI, Arial, sans-serif" font-size="10.5"
            fill="#ffffff">{longest_range}</text>
    </g>

  </g>
</svg>
'''

    with open(out_path, 'w') as f:
        f.write(svg)
    print(out_path, len(svg), 'bytes')
    return svg


if __name__ == '__main__':
    build()
