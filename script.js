(function() {
    const results = {
        modernizr: typeof Modernizr !== "undefined" ? `✔️ Detected (v${Modernizr._version || "unknown"})` : "❌ Not found",
        bootstrap: (() => {
            try {
                if (typeof bootstrap !== "undefined") {
                    return `✔️ Detected (v${bootstrap.Tooltip.VERSION || "5+"})`;
                } else if (typeof $ !== "undefined" && $.fn.tooltip && $.fn.tooltip.Constructor) {
                    return `✔️ Detected (v${$.fn.tooltip.Constructor.VERSION})`;
                } else {
                    return "❌ Not found";
                }
            } catch (e) {
                return "❌ Not found";
            }
        })(),
        html5shiv: (() => {
            const found = [...document.scripts]
                .map(s => s.src)
                .some(src => src.includes("html5shiv"));
            return found ? "✔️ Detected (via script tag)" : "❌ Not found";
        })()
    };
    console.table(results);
})();
