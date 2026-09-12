param([Parameter(Mandatory=$true)][string]$Ch)

# Put the chapter prose on the clipboard and force the Dola Chrome window to the
# foreground. SetForegroundWindow alone is refused when the caller is not already
# foreground, so we attach to the current foreground thread's input queue first.
# Reads from the ASCII-named mirror so this file needs no Korean text.

$path = "H:\YLBooks2\prose\$Ch.txt"
if (-not (Test-Path $path)) { throw "missing: $path" }
$text = [IO.File]::ReadAllText($path)
Set-Clipboard -Value $text

$sig = @'
using System;
using System.Text;
using System.Runtime.InteropServices;
public class DolaWin {
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

  static IntPtr Find(string needle) {
    IntPtr found = IntPtr.Zero;
    EnumWindows((h, l) => {
      var cn = new StringBuilder(256); GetClassName(h, cn, 256);
      if (cn.ToString() != "Chrome_WidgetWin_1") return true;
      var sb = new StringBuilder(512); GetWindowText(h, sb, 512);
      var t = sb.ToString();
      if (t.Length > 0 && t.Contains(needle)) { found = h; return false; }
      return true;
    }, IntPtr.Zero);
    return found;
  }

  public static string Raise(string needle) {
    IntPtr w = Find(needle);
    if (w == IntPtr.Zero) return "not found";
    ShowWindow(w, 9);            // SW_RESTORE
    IntPtr fg = GetForegroundWindow();
    uint tFg = GetWindowThreadProcessId(fg, IntPtr.Zero);
    uint tMe = GetCurrentThreadId();
    uint tTarget = GetWindowThreadProcessId(w, IntPtr.Zero);
    AttachThreadInput(tMe, tFg, true);
    AttachThreadInput(tTarget, tFg, true);
    BringWindowToTop(w);
    SetForegroundWindow(w);
    SetWindowPos(w, new IntPtr(-1), 0, 0, 0, 0, 0x0003);   // HWND_TOPMOST, NOSIZE|NOMOVE
    SetWindowPos(w, new IntPtr(-2), 0, 0, 0, 0, 0x0003);   // HWND_NOTOPMOST
    AttachThreadInput(tTarget, tFg, false);
    AttachThreadInput(tMe, tFg, false);
    return (GetForegroundWindow() == w) ? "foreground" : "still behind";
  }
}
'@
if (-not ("DolaWin" -as [type])) { Add-Type -TypeDefinition $sig }

$state = [DolaWin]::Raise("Dola")
Start-Sleep -Milliseconds 500
"$Ch  chars=$($text.Length)  $state"
