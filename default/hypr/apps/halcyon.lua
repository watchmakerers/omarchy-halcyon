-- Halcyon apps are drawn as classic desktop windows at their own sizes, so they
-- float rather than tile. Media Center is a full-screen 10-foot interface.
o.window(
  "^halcyon-(calendar|chess|dialog|gadgets|games|mail|messenger|mines|navigator|notes|photos|player|search|solitaire|tiles|welcome)$",
  { float = true }
)
o.window("^halcyon-mediacenter$", { fullscreen = true })

-- These draw their own frames, so a floating workspace's titlebar would double up.
-- The rule only exists once the titlebar plugin has loaded, which reloads the config.
if hl.plugin.hyprbars then
  o.window("^halcyon-(gadgets|notes|player)$", { ["hyprbars:no_bar"] = true })
end
