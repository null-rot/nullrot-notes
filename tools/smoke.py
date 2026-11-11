import sys; sys.path.insert(0,'.')
import panel
open('../build/test.html','w').write('<body style="margin:0">'+panel.panel(width_mm=190)+panel.panel({'remain':('hold',1),'sub_pad':('press',2)},crop='lower',width_mm=100)+'</body>')
