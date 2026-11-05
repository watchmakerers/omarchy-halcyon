-- Halcyon apps are drawn as classic desktop windows at their own sizes, so they
-- float rather than tile. Media Center is a full-screen 10-foot interface.
o.window(
  "^halcyon-(calendar|chess|gadgets|games|mail|messenger|mines|navigator|notes|photos|player|search|solitaire|tiles|welcome)$",
  { float = true }
)
o.window("^halcyon-mediacenter$", { fullscreen = true })
