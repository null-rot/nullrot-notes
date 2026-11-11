import sys
from pypdf import PdfReader, PdfWriter, PageObject, Transformation
src, out = sys.argv[1], sys.argv[2]
r = PdfReader(src); N = len(r.pages); assert N % 4 == 0, N
w, h = float(r.pages[0].mediabox.width), float(r.pages[0].mediabox.height)
W = PdfWriter()
def sheet(left, right):
    p = PageObject.create_blank_page(width=2*w, height=h)
    p.merge_transformed_page(r.pages[left-1], Transformation().translate(0, 0))
    p.merge_transformed_page(r.pages[right-1], Transformation().translate(w, 0))
    W.add_page(p)
order = []
for k in range(N // 4):
    order.append((N - 2*k, 2*k + 1))        # front of sheet
    order.append((2*k + 2, N - 2*k - 1))    # back of sheet
for l, rr in order: sheet(l, rr)
W.write(out); print(N, 'pages ->', len(order), 'sides', order)
