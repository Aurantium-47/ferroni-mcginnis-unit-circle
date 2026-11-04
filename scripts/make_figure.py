"""Generate the original explanatory SVG from directly enumerated polynomials.

Numerical root coordinates illustrate the result; they are not certificates.
All SVG geometry is generated here, with no downloaded image/font assets.
"""
from html import escape
from itertools import permutations
from pathlib import Path
import json
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
x, y = sp.symbols('x y')


def polynomial(capacities, cycle_count):
    result = 0
    for perm in permutations(range(len(capacities))):
        seen = set()
        cycle_lengths = []
        for start in range(len(capacities)):
            if start in seen:
                continue
            total, current = 0, start
            while current not in seen:
                seen.add(current)
                total += capacities[current]
                current = perm[current]
            cycle_lengths.append(total)
        if len(cycle_lengths) == cycle_count:
            result += sp.prod(sum(x**j for j in range(a)) for a in cycle_lengths)
    return sp.Poly(result, x)


def roots(poly):
    return sorted((complex(r) for r in poly.nroots(n=35, maxsteps=300)),
                  key=lambda z: (round(z.real, 12), z.imag))


def main():
    equal = polynomial((1, 1, 1, 1, 1, 1), 2)
    unequal = polynomial((1, 2, 3, 4), 2)
    assert equal.as_expr() == 274 + 404*x + 444*x**2 + 404*x**3 + 274*x**4
    transformed = sp.Poly(274*y**4 - 692*y**2 + 184, y)
    ze = roots(equal)
    zu = roots(unequal)
    yt = roots(transformed)
    assert all(abs(r.imag) < 1e-25 and -2 < r.real < 2 for r in yt)
    assert max(abs(abs(r)-1) for r in ze+zu) < 1e-12
    out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 640" role="img" aria-labelledby="title desc">',
           '<title id="title">A path-matrix route to the unit circle</title>',
           '<desc id="desc">Numerical illustrations of four unit-capacity roots on a circle, four roots of the doubled transform in the interval minus two to two, and eight unequal-capacity roots on a circle. The analytic proof uses a path determinant, real-root localization, and polarization.</desc>',
           '<rect width="1200" height="640" rx="24" fill="#101b2c"/>',
           '<style>text{font-family:Arial,Helvetica,sans-serif}.label{fill:#e9eef7;font-size:18px}.muted{fill:#aebed5;font-size:16px}.title{fill:#f6f8fc;font-weight:700}.axis{stroke:#7890ac;stroke-width:1.4}.panel{fill:#18273d;stroke:#30435d;stroke-width:1.2}</style>']

    def text(tx, ty, content, cls='label', extra=''):
        out.append(f'<text x="{tx}" y="{ty}" class="{cls}" {extra}>{escape(content)}</text>')

    text(42, 52, 'A path-matrix route to the unit circle', 'title', 'font-size="30"')
    text(42, 82, 'Ferroni–McGinnis Conjecture 4.5  ·  positive integer capacities', 'muted')
    panels = [(32, '#75bfff', '1', 'UNIT CAPACITIES'), (428, '#c3a6ff', '2', 'REAL-ROOT LOCALIZATION'), (824, '#ffc477', '3', 'ARBITRARY CAPACITIES')]
    for px, color, num, heading in panels:
        out.append(f'<rect x="{px}" y="108" width="344" height="422" rx="16" class="panel"/>')
        out.append(f'<circle cx="{px+28}" cy="139" r="13" fill="{color}"/>')
        text(px+28, 145, num, 'title', 'font-size="16" text-anchor="middle" style="fill:#101b2c"')
        text(px+50, 145, heading, 'title', 'font-size="14"')

    def circle_plot(cx, cy, rs, color):
        scale=100
        out.append(f'<line x1="{cx-125}" y1="{cy}" x2="{cx+125}" y2="{cy}" class="axis"/>')
        out.append(f'<line x1="{cx}" y1="{cy-125}" x2="{cx}" y2="{cy+125}" class="axis"/>')
        out.append(f'<circle cx="{cx}" cy="{cy}" r="{scale}" fill="none" stroke="{color}" stroke-width="2" opacity="0.8"/>')
        text(cx+111, cy+20, 'Re', 'muted', 'font-size="13"')
        text(cx+9, cy-112, 'Im', 'muted', 'font-size="13"')
        text(cx+100, cy-10, '1', 'muted', 'font-size="13"')
        for r in rs:
            out.append(f'<circle cx="{cx+scale*r.real:.6f}" cy="{cy-scale*r.imag:.6f}" r="5.5" fill="{color}" stroke="#101b2c" stroke-width="1.8"/>')

    circle_plot(204, 308, ze, '#75bfff')
    text(204, 440, 'n = 6, k = 2', 'label', 'text-anchor="middle"')
    text(204, 468, 'c = (1, 1, 1, 1, 1, 1)', 'muted', 'text-anchor="middle"')
    text(204, 500, '4 zeros on |x| = 1', 'label', 'text-anchor="middle"')

    # A tiny path visually identifies the tridiagonal matrix.
    for j in range(4):
        out.append(f'<line x1="{502+49*j}" y1="218" x2="{551+49*j}" y2="218" stroke="#c3a6ff" stroke-width="3"/>')
    for j in range(5):
        out.append(f'<circle cx="{502+49*j}" cy="218" r="7" fill="#c3a6ff"/>')
    text(600, 254, 'path adjacency matrix T₅', 'muted', 'text-anchor="middle"')
    out.append('<line x1="468" y1="327" x2="732" y2="327" stroke="#c3a6ff" stroke-width="3"/>')
    for endpoint in [468,732]:
        out.append(f'<circle cx="{endpoint}" cy="327" r="5" fill="#18273d" stroke="#c3a6ff" stroke-width="2"/>')
    for r in yt:
        out.append(f'<circle cx="{600+66*r.real:.6f}" cy="327" r="6" fill="#c3a6ff" stroke="#101b2c" stroke-width="1.6"/>')
    text(468, 355, '−2', 'muted', 'text-anchor="middle"')
    text(600, 355, '0', 'muted', 'text-anchor="middle"')
    text(732, 355, '2', 'muted', 'text-anchor="middle"')
    text(600, 400, 'y = z + 1/z,   x = z²', 'label', 'text-anchor="middle"')
    text(600, 440, '274y⁴ − 692y² + 184', 'label', 'text-anchor="middle"')
    text(600, 468, 'real roots strictly in (−2, 2)', 'muted', 'text-anchor="middle"')
    text(600, 500, 'Gauss–Lucas + minor signs', 'label', 'text-anchor="middle"')

    circle_plot(996, 308, zu, '#ffc477')
    text(996, 440, 'n = 4, k = 2', 'label', 'text-anchor="middle"')
    text(996, 468, 'c = (1, 2, 3, 4)', 'muted', 'text-anchor="middle"')
    text(996, 500, '8 zeros on |x| = 1', 'label', 'text-anchor="middle"')
    text(600, 568, 'Known recurrence  →  path determinant  →  disk polarization  →  reciprocity', 'label', 'text-anchor="middle" font-size="17"')
    text(600, 605, 'Dots are numerical illustrations. The general conclusion comes from the analytic proof.', 'muted', 'text-anchor="middle" font-size="15"')
    out.append('</svg>')
    (ROOT/'assets').mkdir(exist_ok=True)
    (ROOT/'assets'/'proof-map.svg').write_text('\n'.join(out)+'\n', encoding='utf-8')
    data = {'purpose':'Numerical illustration only, not a proof or root certificate.', 'sympy':sp.__version__, 'examples':[]}
    for capacities, k, poly, rr in [((1,)*6,2,equal,ze),((1,2,3,4),2,unequal,zu)]:
        data['examples'].append({'capacities':list(capacities),'cycle_count':k,'coefficients_ascending':[int(v) for v in reversed(poly.all_coeffs())], 'roots_approximate':[{'real':format(r.real,'.15g'),'imaginary':format(r.imag,'.15g')} for r in rr]})
    (ROOT/'assets'/'example-data.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    print('Generated assets/proof-map.svg and assets/example-data.json')


if __name__ == '__main__':
    main()
