# Clear the clipboard and force the Dola Chrome window to the foreground so the
# next synthetic click lands. Run this right before clicking the copy button.

Set-Clipboard -Value "EMPTY_MARKER"

$sig = @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public class DolaRaise {
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc cb, IntPtr l);
  [DllImport("user32.dll")] static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] static extern int GetClassName(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] static extern bool ShowWindow(IntPtr h, int c);
  [DllImport("user32.dll")] static extern bool BringWindowToTop(IntPtr h);
  [DllImport("user32.dll")] static extern bool AttachThreadInput(uint a, uint b, bool attach);
  [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, IntPtr pid);
  [DllImport("kernel32.dll")] static extern uint GetCurrentThreadId();
  [DllImport("user32.dll")] static extern bool SetWindowPos(IntPtr h, IntPtr after, int x, int y, int cx, int cy, uint flags);

  public static string Raise(string needle) {
    IntPtr w = IntPtr.Zero;
    EnumWindows((h, l) => {
      var cn = new StringBuilder(256); GetClassName(h, cn, 256);
      if (cn.ToString() != "Chrome_WidgetWin_1") return true;
      var sb = new StringBuilder(512); GetWindowText(h, sb, 512);
      if (sb.Length > 0 && sb.ToString().Contains(needle)) { w = h; return false; }
      return true;
    }, IntPtr.Zero);
    if (w == IntPtr.Zero) return "not found";
    ShowWindow(w, 9);
    IntPtr fg = GetForegroundWindow();
    uint tFg = GetWindowThreadProcessId(fg, IntPtr.Zero);
    uint tMe = GetCurrentThreadId();
    uint tTarget = GetWindowThreadProcessId(w, IntPtr.Zero);
    AttachThreadInput(tMe, tFg, true);
    AttachThreadInput(tTarget, tFg, true);
    BringWindowToTop(w);
    SetForegroundWindow(w);
    SetWindowPos(w, new IntPtr(-1), 0, 0, 0, 0, 0x0003);
    SetWindowPos(w, new IntPtr(-2), 0, 0, 0, 0, 0x0003);
    AttachThreadInput(tTarget, tFg, false);
    AttachThreadInput(tMe, tFg, false);
    return (GetForegroundWindow() == w) ? "foreground" : "still behind";
  }
}
'@
if (-not ("DolaRaise" -as [type])) { Add-Type -TypeDefinition $sig }

$state = [DolaRaise]::Raise("Dola")
Start-Sleep -Milliseconds 500
"clipboard cleared; window $state"
