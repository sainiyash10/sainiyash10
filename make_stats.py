import math

W, H = 495, 195
RX = 16


def build(stars=2, commits=4, repos=2, followers=1, rank="C", rank_pct=40, out_path='assets/stats.svg'):
    r = 46
    circumf = 2 * math.pi * r  # 289.03
    dash = circumf * rank_pct / 100

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <!-- Background gradient -->
    <linearGradient id="sBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#1f0f38"/>
      <stop offset="100%" stop-color="#140823"/>
    </linearGradient>
    <!-- Border / ring gradient -->
    <linearGradient id="sRing" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ff5fc4"/>
      <stop offset="100%" stop-color="#a259ff"/>
    </linearGradient>
    <!-- Title gradient text -->
    <linearGradient id="titleGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#ff5fc4"/>
      <stop offset="60%" stop-color="#f9e84a"/>
    </linearGradient>
    <clipPath id="sClip">
      <rect width="{W}" height="{H}" rx="{RX}"/>
    </clipPath>
  </defs>

  <g clip-path="url(#sClip)">
    <!-- Background -->
    <rect width="{W}" height="{H}" fill="url(#sBg)"/>

    <!-- Border with gradient -->
    <rect x="0.75" y="0.75" width="{W-1.5}" height="{H-1.5}" rx="15.5" fill="none"
          stroke="#a259ff" stroke-width="1.6"/>

    <!-- Title row -->
    <text x="24" y="36" font-family="Segoe UI, Arial, sans-serif" font-size="15" font-weight="700"
          fill="#ff5fc4">Yash Saini's GitHub Stats</text>

    <!-- \u2500\u2500\u2500 Stats rows \u2500\u2500\u2500 -->

    <!-- Row 1: Stars -->
    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.15s" fill="freeze"/>
      <text x="24" y="74" font-family="Segoe UI, Arial, sans-serif" font-size="14">\u2b50</text>
      <text x="46" y="74" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#c9a9e9">Total Stars Earned:</text>
      <text x="230" y="74" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="700" fill="#f9e84a">{stars}</text>
    </g>

    <!-- Row 2: Commits -->
    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.35s" fill="freeze"/>
      <text x="24" y="101" font-family="Segoe UI, Arial, sans-serif" font-size="14">\U0001f4bb</text>
      <text x="46" y="101" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#c9a9e9">Total Commits:</text>
      <text x="230" y="101" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="700" fill="#3de8c8">{commits}</text>
    </g>

    <!-- Row 3: Public Repos -->
    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.55s" fill="freeze"/>
      <text x="24" y="128" font-family="Segoe UI, Arial, sans-serif" font-size="14">\U0001f4e6</text>
      <text x="46" y="128" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#c9a9e9">Public Repos:</text>
      <text x="230" y="128" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="700" fill="#4dfa90">{repos}</text>
    </g>

    <!-- Row 4: PRs -->
    <g opacity="0">
      <animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="0.75s" fill="freeze"/>
      <text x="24" y="155" font-family="Segoe UI, Arial, sans-serif" font-size="14">\U0001f465</text>
      <text x="46" y="155" font-family="Segoe UI, Arial, sans-serif" font-size="13" fill="#c9a9e9">Followers:</text>
      <text x="230" y="155" font-family="Segoe UI, Arial, sans-serif" font-size="13" font-weight="700" fill="#c084fc">{followers}</text>
    </g>

    <!-- \u2500\u2500\u2500 Rank ring (right side) \u2500\u2500\u2500 -->
    <g transform="translate(413, 97)">
      <!-- Track ring -->
      <circle r="46" fill="none" stroke="rgba(255,255,255,0.10)" stroke-width="9"/>
      <!-- Animated gradient arc \u2014 A+ rank ~ 92% \u2192 dasharray 265/289 -->
      <circle r="46" fill="none" stroke="url(#sRing)" stroke-width="9"
              stroke-linecap="round" stroke-dasharray="0 {circumf:.2f}"
              transform="rotate(-90)">
        <animate attributeName="stroke-dasharray"
                 from="0 {circumf:.2f}" to="{int(dash)} {circumf:.2f}"
                 dur="1.4s" begin="0.3s" fill="freeze"
                 calcMode="spline" keySplines="0.2 0.6 0.25 1"/>
      </circle>
      <!-- Grade letter -->
      <text x="0" y="8" text-anchor="middle" font-family="Segoe UI, Arial, sans-serif" font-size="26" font-weight="800" fill="#f3e8ff" opacity="0">
        {rank}
        <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="1.1s" fill="freeze"/>
      </text>
    </g>

  </g>
</svg>'''

    with open(out_path, 'w') as f:
        f.write(svg)
    print(out_path, len(svg), 'bytes')
    return svg


if __name__ == '__main__':
    build()
