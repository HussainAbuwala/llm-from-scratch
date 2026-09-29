"""Small editable math layout for this episode's formulas (no runtime web fonts)."""
from excalidraw_kit import text, line, CODE

# Nodes store their width and drawable parts relative to a common text baseline.
def literal(value, size=36):
    return (len(value)*size*.60, [('text', 0, -size*.95, value, size)])


def row(*nodes):
    width, parts = 0, []
    for w, elements in nodes:
        parts.extend((kind, x+width, y, value, size) for kind,x,y,value,size in elements)
        width += w
    return width, parts


def offset(node, dx=0, dy=0):
    return [(kind,x+dx,y+dy,value,size) for kind,x,y,value,size in node[1]]


def sub(base, index, size=36):
    a,b=literal(base,size),literal(index,size*.62)
    return a[0]+b[0]+3, a[1]+offset(b,a[0]+2,size*.23)


def power(base, exponent, size=36):
    a=literal(base,size)
    return a[0]+exponent[0]+2, a[1]+offset(exponent,a[0]+1,-size*.48)


def summation(index, size=36):
    a,b=literal('∑',size*1.12),literal(index,size*.53)
    # Leave a visible gap below the summation glyph, including its descender.
    return a[0]+12,a[1]+offset(b,(a[0]-b[0])/2,size*.82)


def fraction(top,bottom):
    w=max(top[0],bottom[0])+24
    # Fraction bar lies on the math axis; numerator and denominator have room
    # for their own subscripts, superscripts and summation indices.
    return w, offset(top,(w-top[0])/2,-36)+offset(bottom,(w-bottom[0])/2,28)+[('line',0,-16,w,2)]


def formula(name):
    t=literal
    sj,sk,pj=sub('s','j'),sub('s','k',24),sub('p','j')
    ej=power('e',sub('s','j',24))
    ek=power('e',sk)
    denominator=row(summation('k'),ek)
    if name=='shift': return row(sj,t(' = '),sub('z','j'),t(' − max(z)'))
    if name=='softmax': return row(pj,t(' = '),fraction(ej,denominator))
    if name=='log_softmax': return row(t('ln('),pj,t(') = '),sj,t(' − ln('),denominator,t(')'))
    if name=='target': return t('y = [0, 0, 0, 1]')
    if name=='cross_entropy':
        return row(t('L = −'),summation('j'),sub('y','j'),t(' ln('),pj,t(') = −ln('),sub('p','END'),t(')'))
    if name=='target_loss': return row(t('L = −ln('),fraction(t('2',30),t('5',30)),t(') ≈ 0.916291 nats'))
    if name=='baseline_average': return row(t('L = '),fraction(t('5 ln 4 + 4 ln 4',32),t('9',32)),t(' = ln 4 ≈ 1.386294',32))
    if name=='row_mean': return row(sub('L','a'),t(' = '),fraction(t('2 ln 5 + 2 ln(5/2)',32),t('4',32)))
    raise ValueError(name)


def draw_formula(scene,name,x,y,width):
    node=formula(name)
    assert node[0]<width-40,(name,node[0],width)
    left=x+(width-node[0])/2
    for kind,dx,dy,value,size in node[1]:
        if kind=='text': scene.add(text(left+dx,y+dy,value,size,CODE))
        else: scene.add(line([(left+dx,y+dy),(left+dx+value,y+dy)],sw=size,roughness=0))
