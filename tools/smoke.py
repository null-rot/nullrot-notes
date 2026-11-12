import sys; sys.path.insert(0,'.')
import devices, panel
devices.use('sp404mk2')
open('../build/test.html','w',encoding='utf-8').write('<body style="margin:0">'+panel.panel(width_mm=190)+panel.panel({'remain':('hold',1),'sub_pad':('press',2)},crop='lower',width_mm=100)+'</body>')
