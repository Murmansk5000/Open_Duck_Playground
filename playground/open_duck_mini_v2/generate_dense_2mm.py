#!/usr/bin/env python3
"""Generate custom obstacle terrain XML: dense 2mm strips with 3mm gaps."""

strip_half_width = 0.0025   # 2.5mm half-width (5mm full width)
strip_half_height = 0.001   # 1mm half-height (2mm full height)
strip_half_length = 1.5     # 1.5m half-length
gap = 0.003                 # 3mm gap
period = 2 * strip_half_width + gap  # 8mm period

x_min, x_max = -1.5, 1.5
safe_min, safe_max = -0.08, 0.08  # Safe spawn area

header = '''<mujoco model="Dense 2mm Obstacles (3mm gap)">
    <include file="open_duck_mini_v2.xml"/>

    <visual>
        <headlight diffuse="0.6 0.6 0.6" ambient="0.3 0.3 0.3" specular="0 0 0"/>
        <rgba haze="0.15 0.25 0.35 1"/>
        <global azimuth="160" elevation="-20"/>
    </visual>

    <asset>
        <texture type="skybox" builtin="gradient" rgb1="0.3 0.5 0.7" rgb2="0 0 0" width="512" height="3072"/>
        <texture type="2d" name="groundplane" builtin="checker" mark="edge"
                 rgb1="0.8 0.8 0.8" rgb2="0.7 0.7 0.7"
                 markrgb="0.6 0.6 0.6" width="300" height="300"/>
        <material name="groundplane" texture="groundplane" texuniform="true"
                  texrepeat="10 10" reflectance="0.2"/>
        <material name="bump_mat" rgba="0.7 0.6 0.5 1"/>
    </asset>

    <worldbody>
        <body name="floor">
            <geom name="floor" size="20 20 0.01" type="plane" material="groundplane"
                  contype="1" conaffinity="0" priority="1" friction="0.8" condim="3"/>
        </body>

'''

footer = '''    </worldbody>

    <keyframe>
        <key name="home"
             qpos="0 0 0.15 1 0 0 0 0.002 0.053 -0.63 1.368 -0.784 0 0 0 0 -0.003 -0.065 0.635 1.379 -0.796"
             ctrl="0.002 0.053 -0.63 1.368 -0.784 0 0 0 0 -0.003 -0.065 0.635 1.379 -0.796"/>
    </keyframe>
</mujoco>
'''

import os

lines = []
x, i = x_min, 1
while x <= x_max:
    if safe_min < x < safe_max:
        x += period
        continue
    lines.append(
        f'        <geom name="strip_{i:03d}" type="box" '
        f'size="{strip_half_width} {strip_half_length} {strip_half_height}" '
        f'pos="{x:.4f} 0.0 {strip_half_height}" material="bump_mat" friction="0.8"/>'
    )
    i += 1
    x += period

output_path = os.path.join(os.path.dirname(__file__), "xmls", "scene_dense_2mm.xml")
with open(output_path, "w") as f:
    f.write(header + "\n".join(lines) + "\n" + footer)

print(f"Generated {i - 1} obstacle strips -> {output_path}")
