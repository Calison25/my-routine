```markdown
# Design System Specification: Premium Dark Athleticism

## 1. Overview & Creative North Star: "The Neon Sanctuary"
This design system is built for the high-performance athlete who seeks mental clarity and intense focus. We are moving away from the "bright and airy" fitness aesthetic toward a **"Neon Sanctuary"**—a deep, immersive environment where the UI recedes into the background, leaving only the essential data and kinetic energy of the workout.

To break the "standard template" look, this system utilizes **intentional asymmetry** and **tonal depth**. We avoid the rigid 12-column grid in favor of an editorial-style layout where white space (or in this case, "dark space") is treated as a premium element. Large, high-contrast typography scales create a sense of authority, while teal accents provide a rhythmic "pulse" through the interface.

---

## 2. Colors & Surface Philosophy
The palette is rooted in a deep slate (`#0b1326`), utilizing high-vibrancy cyan and teal tokens to draw the eye to critical performance metrics.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders for sectioning. Structural boundaries must be defined solely through background color shifts. For example, a `surface-container-low` section sitting on a `surface` background provides all the definition needed. If you feel the urge to draw a line, use 48px of vertical padding instead.

### Surface Hierarchy & Nesting
Treat the UI as a series of physical layers, like stacked sheets of obsidian or frosted glass.
- **Base Layer:** `surface` (`#0b1326`) for the main background.
- **Secondary Areas:** `surface-container-low` (`#131b2e`) for secondary content zones.
- **Interactive Cards:** `surface-container-high` (`#222a3d`) to bring data forward.
- **The Glass & Gradient Rule:** For floating action elements, use a backdrop-blur (12px–20px) with `surface-variant` at 60% opacity. For main CTAs, use a linear gradient from `primary` (`#47eaed`) to `primary-container` (`#00ced1`) to provide a "lit-from-within" glow.

---

## 3. Typography: The Manrope Editorial
We use **Manrope** exclusively. Its geometric yet approachable nature feels modern and mechanical.

*   **Display (lg/md/sm):** Used for singular, high-impact data points (e.g., Heart Rate, Total Weight). Use `display-lg` (3.5rem) with `-0.04em` letter spacing to create a "brutal" premium look.
*   **Headlines:** Used for section titles. `headline-sm` (1.5rem) should always be in `on-surface`.
*   **Titles:** Use `title-lg` for card headers.
*   **Body:** `body-md` (0.875rem) is our workhorse. Ensure `on-surface-variant` is used for secondary body text to maintain hierarchy.
*   **Labels:** `label-sm` (0.6875rem) should be used for uppercase metadata with `+0.05em` tracking to provide an "engineered" feel.

---

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows have no place here. We achieve depth through the **Layering Principle**.

*   **Ambient Shadows:** If a floating element (like a workout-pause modal) requires a shadow, it must be massive and faint. Use a 64px blur, 0% spread, and the color of the `on-surface` token at 4% opacity. This mimics a soft glow rather than a harsh shadow.
*   **The "Ghost Border" Fallback:** If accessibility requires a container boundary, use the `outline-variant` (`#3b4949`) at 20% opacity. This creates a suggestion of an edge without breaking the "No-Line" rule.
*   **Kinetic Glow:** Use `primary` or `secondary` tokens as small, blurred decorative "orbs" behind key stats to create a sense of atmospheric depth.

---

## 5. Components & Interaction

### Buttons
*   **Primary:** A solid `primary` (`#47eaed`) fill with `on-primary` text. Use `full` roundedness (9999px) for a "pill" shape that feels ergonomic.
*   **Secondary:** No fill. Use a "Ghost Border" (20% `outline-variant`) and `primary` text.
*   **Tertiary:** Text only in `primary`, no background, with `label-md` styling.

### Cards & Progress
*   **Performance Cards:** Forbid dividers. Use `surface-container-highest` (`#2d3449`) backgrounds. 
*   **The Progress Ring:** Utilize the `primary` to `secondary` gradient for progress bars. The "track" of the bar should be `surface-container-lowest` to look like it is recessed into the screen.

### Input Fields
*   **Styling:** Use `surface-container-low` as the field background. No border. The active state is indicated by a 2px `primary` bottom-border only, creating a clean, architectural look.
*   **Error State:** Use `error` (`#ffb4ab`) sparingly.

### Specialized Athletic Components
*   **The Pulse Meter:** A micro-interaction component using a soft `surface-tint` glow that expands and contracts behind the BPM display.
*   **Set Selectors:** Use `md` (0.375rem) roundedness for set selection chips. Selected state uses `primary-container`, unselected uses `surface-container-high`.

---

## 6. Do’s and Don'ts

### Do:
*   **Do** use extreme scale. A 3.5rem BPM next to a 0.6875rem label creates a high-end, intentional contrast.
*   **Do** embrace the void. Use large areas of `surface` color to allow the athlete to focus on their form, not the UI.
*   **Do** use `primary` sparingly. It should feel like a neon light in a dark room—purposeful and striking.

### Don't:
*   **Don't** use 100% white (`#FFFFFF`). Always use `on-surface` (`#dae2fd`) to prevent eye strain in low-light gym environments.
*   **Don't** use standard Material Design dividers. If you need to separate content, use an 8px vertical gap or a subtle shift from `surface-container-low` to `surface-container-high`.
*   **Don't** use sharp corners. Stick to the `md` (0.375rem) and `lg` (0.5rem) tokens to keep the interface feeling premium and tactile.