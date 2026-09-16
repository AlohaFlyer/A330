"""Alaska (as787pilot.app) hex -> Hawaiian (ha330pilot.app) hex.
Role-based. Semantic colors (red, amber, success green, flow phase colors,
podcast tab accents, Jeopardy board) are deliberately NOT in this map.
Source palette: Auro design tokens, Hawaiian theme, verified 2026-09-01.
"""
DARK_FAMILY = {'limitations','memory-items','triggers','weather','hot-seat','limit-or-bust',
               'wx-alternate','ioe','podcast','view','systems_quiz'}

# Unambiguous, context-free replacements (lowercase keys).
MAP = {
  # brand dark
  '#01416e':'#463C8F', '#01426a':'#463C8F',
  # atlas / links / hover accents (background context handled in apply)
  '#00679c':'#CE0C88', '#0074c8':'#CE0C88', '#007cba':'#CE0C88', '#0086e6':'#CE0C88',
  '#00b2d6':'#E26DB8', '#00c7e6':'#E26DB8', '#5090d0':'#E26DB8', '#6aa0e0':'#E26DB8',
  '#7fc4f0':'#E26DB8', '#3a93d8':'#E26DB8', '#0a8fb0':'#CE0C88', '#0a6e8f':'#831A57',
  '#0b7285':'#831A57', '#1d63b0':'#463C8F', '#1864ab':'#463C8F', '#0a6c8f':'#831A57',
  # pale tints
  '#bfe9f4':'#EAE5F4', '#e8f3fa':'#F4F1F9', '#e8f2f9':'#F4F1F9', '#eef4f8':'#F1EEF6',
  '#d6ecf7':'#FDF1F8', '#efe3f5':'#EAE5F4', '#f4f9fc':'#F7F5FB', '#cfe3f5':'#EAE5F4',
  '#d7e1ea':'#DBDDDD', '#e1eaf2':'#E4E0EC', '#bcd6ec':'#EAE5F4', '#dfe8f0':'#E9E5F1',
  '#e6edf3':'#E6E3EE', '#f1f6fb':'#F4F1F9', '#d7e9fb':'#EAE5F4', '#e4eef5':'#EAE5F4',
  '#eaf4fc':'#F4F1F9', '#dcecf8':'#EAE5F4', '#cfe1f0':'#DBD6E8', '#cfe3ef':'#DBD6E8',
  '#b9d4e3':'#D3CDE3', '#cfe0ee':'#EAE5F4', '#7fd4ef':'#E26DB8', '#8fd9ef':'#E26DB8',
  '#a9b8e8':'#D3C9F0',
  # neutral blue-greys -> purple-greys
  '#7d99ac':'#8C8798', '#6f8aa0':'#6F6B7E', '#7a94a3':'#6F6B7E', '#7a93a4':'#6F6B7E',
  '#5b7a8c':'#6F6B7E', '#9ab3c4':'#A29DB0', '#5c728a':'#6F6B7E', '#9bb8c9':'#A29DB0',
  '#4a8aa0':'#8C7EB8', '#6f93b0':'#8C8798', '#9fb3c0':'#A29DB0', '#557':'#5A5670',
  '#9bb1c4':'#A29DB0', '#6b7280':'#6F6B7E',
  # inks on light
  '#15314a':'#1E1A2E', '#334e68':'#3A3550', '#12303f':'#1E1A2E', '#16313f':'#1E1A2E',
  '#06243b':'#1E1A2E', '#243b47':'#2A2440',
  # dark drill family
  '#01172b':'#1A1630', '#062b46':'#2A2440', '#0a3556':'#332E44', '#13486e':'#453F58',
  '#0c3a5e':'#4A4460', '#02101f':'#120F1F', '#01233b':'#201B33', '#02233b':'#1A1630',
  '#8fb3cf':'#C3BED0', '#cfe2f2':'#DCD8E6', '#eaf3fb':'#F1EEF6', '#c0e585':'#8EC891',
  '#04121f':'#120F1F', '#2a4761':'#3A3550',
  # ioe dark
  '#0b1c2c':'#1A1630', '#12293d':'#2A2440', '#1e3d57':'#453F58', '#eaf2f8':'#F1EEF6',
  '#9ab4c8':'#C3BED0', '#0e2233':'#211D2E', '#0a1a27':'#15131C', '#2a3550':'#332E44',
  # systems dark
  '#0a0d12':'#15131C', '#141820':'#211D2E', '#1c2230':'#2A2440', '#2a3344':'#453F58',
  '#d8dde8':'#EDE9F3', '#7a8899':'#A29DB0', '#0d1520':'#1A1630', '#a0b8d0':'#C3BED0',
  '#2a4060':'#3A3550',
  # view
  '#0a1b2c':'#15131C',
  # phase_flows dark theme
  '#0d1620':'#15131C', '#15212d':'#211D2E', '#26384a':'#453F58', '#06243a':'#2A2440',
  '#101c28':'#1A1630', '#1b2a38':'#2A2440', '#e7eff7':'#EDE9F3', '#0f1d29':'#1A1630',
}

# #b1d887 (Alaska lime) by role. Text on dark surfaces -> coral tint.
LIME = '#b1d887'
LIME_TEXT_ON_DARK = '#FF9080'   # 4.3:1 on #463C8F
LIME_FILL_ON_LIGHT = '#FFC9BF'  # purple text on it 6.1:1
LIME_BORDER_ON_LIGHT = '#EE453D'
LIME_SUCCESS = '#8EC891'        # where lime meant "done / correct"

# Per-file overrides applied BEFORE the generic map (exact substring -> replacement).
OVERRIDES = {
  'portal-settings.js': [
    # log button and no-tax box are a green scheme, keep them green
    ('background:#eaf7db;border:2px solid #b1d887;color:#4a7a1f', 'background:#D6EAC7;border:2px solid #8EC891;color:#447A1F'),
    ('.ps-logbtn:hover{background:#b1d887;color:#2f4f12;}', '.ps-logbtn:hover{background:#8EC891;color:#2E5214;}'),
    ('.ps-free{background:#eaf7db;border-left:4px solid #b1d887;', '.ps-free{background:#D6EAC7;border-left:4px solid #8EC891;'),
    ('.ps-logbtn svg{color:#7fb440;}', '.ps-logbtn svg{color:#5DB060;}'),
    ('.ps-logbtn:hover svg{color:#2f4f12;}', '.ps-logbtn:hover svg{color:#2E5214;}'),
  ],
  'index.html': [
    # banner title (text on purple) and .phase tile (fill on white) shared --good
    ('.banner span{color:var(--good);', '.banner span{color:var(--goodtext);'),
    ('--good:#b1d887;}', '--good:#FFC9BF;--goodtext:#FF9080;}'),
  ],
  'flows_quiz.html': [
    # PF/PM dot roles: PF would collide with FO fuchsia after the map
    ('svg .dot.rolePF{fill:#007cba;stroke:#01416e;}', 'svg .dot.rolePF{fill:#00805E;stroke:#1C4A0C;}'),
    ('svg .dot.rolePM{fill:#00b2d6;stroke:#0a8fb0;}', 'svg .dot.rolePM{fill:#E26DB8;stroke:#831A57;}'),
    ('<i style="background:#007cba;border-color:#01416e"></i>PF', '<i style="background:#00805E;border-color:#1C4A0C"></i>PF'),
    ('<i style="background:#00b2d6;border-color:#0a8fb0"></i>PM', '<i style="background:#E26DB8;border-color:#831A57"></i>PM'),
    ('--good:#b1d887', '--good:#8EC891'),
  ],
  'fom_quiz.html': [('--good:#b1d887', '--good:#8EC891')],
  'jeopardy.html': [('--green:#b1d887', '--green:#8EC891')],
  'mcdu_preflight.html': [('#0a8fb0', '#831A57')],   # page-flow group 4 stays distinct from group 1
}
