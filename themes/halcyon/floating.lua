-- Floating workspaces in the Halcyon look. Solid colors, so a titlebar keeps the
-- theme's color over any wallpaper.
local button_border = "rgba(000a14cc)"

return {
  rounding = 8,

  shadow = { enabled = true, range = 22, render_power = 3, color = "rgba(00203a80)" },

  titlebar = {
    bar_height = 30,
    bar_color = "rgb(1a5f94)",
    bar_color_inactive = "rgb(123a5c)",
    col = { text = "rgb(ffffff)" },
    bar_text_font = "Source Sans 3",
    bar_text_size = 12,
    bar_text_weight = "semibold",
    bar_button_padding = 6,
    button_rounding = 6,
    button_border_size = 1,
    button_border_color = button_border,
    inactive_button_color = "rgb(3f6f92)",
  },

  buttons = {
    close = { bg_color = "rgb(d9432f)", fg_color = "rgb(ffffff)", size = 20 },
    maximize = { bg_color = "rgb(2a8fd0)", fg_color = "rgb(ffffff)", size = 20 },
    minimize = { bg_color = "rgb(2a8fd0)", fg_color = "rgb(ffffff)", size = 20 },
  },
}
