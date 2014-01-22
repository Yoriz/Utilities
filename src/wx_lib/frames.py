'''
Created on 25 Jan 2013

@author: Dave Wilson
'''

import wx
import enhanced_status_bar


FRAME_STYLE = (wx.FRAME_FLOAT_ON_PARENT | wx.SYSTEM_MENU | wx.CAPTION |
                        wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX |
                        wx.CLIP_CHILDREN | wx.FRAME_NO_TASKBAR)

FRAME_DIALOG_STYLE = (wx.FRAME_FLOAT_ON_PARENT | wx.CAPTION |
                      wx.FRAME_NO_TASKBAR)
FRAME_DIALOG_STYLE2 = (FRAME_DIALOG_STYLE | wx.SYSTEM_MENU | wx.CLOSE_BOX)

FRAME_DIALOG_STYLE3 = (FRAME_DIALOG_STYLE2 | wx.RESIZE_BORDER |
                       wx.MAXIMIZE_BOX | wx.RESIZE_BOX)


class GaugeStatusBar(enhanced_status_bar.EnhancedStatusBar):
    def __init__(self, parent):
        super(GaugeStatusBar, self).__init__(parent, style=wx.SB_FLAT)
        self.SetSize((-1, 23))
        self.SetFieldsCount(2)
        self.SetStatusWidths([-1, 100])

        self.progress_gauge = wx.Gauge(self, size=(100, 15))
        self.progress_gauge.Show(False)
        self.AddWidget(self.progress_gauge, pos=1)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._on_timer)

    def _on_timer(self, event):
        self.progress_gauge.Pulse()

    def pulse_gauge(self, pulse=True):
        isRunning = self.timer.IsRunning()
        if not isRunning and pulse:
            self.timer.Start(500)
        elif isRunning and not pulse:
            self.timer.Stop()
        self.progress_gauge.Show(pulse)


class GaugeFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super(GaugeFrame, self).__init__(*args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.panel = wx.Panel(self)
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.statusBar = GaugeStatusBar(self)
        self.SetStatusBar(self.statusBar)

    @classmethod
    def modal(cls, *args, **kwargs):
        if not kwargs.get('style'):
            kwargs['style'] = FRAME_DIALOG_STYLE2
        gauge_frame = cls(*args, **kwargs)
        gauge_frame.CenterOnParent()
        gauge_frame.MakeModal()
        gauge_frame.Bind(wx.EVT_CLOSE, gauge_frame.close_modal)
        return gauge_frame

    @classmethod
    def modal_resize(cls, *args, **kwargs):
        kwargs['style'] = FRAME_DIALOG_STYLE3
        return cls.modal(*args, **kwargs)

    def close_modal(self, event):
        event.Skip()
        self.MakeModal(False)
        self.Destroy()

    def set_panel(self, panel):
        self.Freeze()
        self.panel.Destroy()
        self.panel = panel
        self.sizer.Add(self.panel, 1, wx.EXPAND)
        self.Layout()
        self.Thaw()

    def set_gauge_pulse(self, pulse=True):
        self.statusBar.pulse_gauge(pulse)

    def set_status_text(self, status_text=''):
        self.statusBar.SetStatusText(status_text)

    def set_gauge_and_status_text(self, pulse=True, status_text=''):
        self.set_gauge_pulse(pulse)
        self.set_status_text(status_text)

    def show_error_dialog(self, title_text, error_text, icon=None):
#         title_text, error_text = str(title_text), str(error_text)
        if not icon:
            icon = wx.ICON_ERROR
        elif icon == 'information':
            icon = wx.ICON_INFORMATION
        dialog = wx.MessageDialog(self, error_text, title_text,
                                  icon | wx.OK | wx.CENTER)
        dialog.ShowModal()
        dialog.Destroy()

    def set_panel_enable(self, enable=True):
        self.panel.Enable(enable)


if __name__ == '__main__':
    wx_app = wx.App(None)
    frame = GaugeFrame(None, title='Testing GaugeFrame')
    frame.Show()
    frame.set_gauge_and_status_text(True, 'Test status')
    wx_app.MainLoop()
