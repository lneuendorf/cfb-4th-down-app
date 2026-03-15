(function () {
    const EXPORT_SCALE = 2;
    const EXPORT_TITLE_FONT_SIZE = 16;
    const EXPORT_SUBTITLE_FONT_SIZE = 16;

    function sanitizeFilename(name) {
        return (name || "chart")
            .toLowerCase()
            .replace(/<[^>]+>/g, "")
            .replace(/[^a-z0-9]+/g, "-")
            .replace(/^-+|-+$/g, "");
    }

    function escapeHtml(text) {
        return String(text || "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#39;");
    }

    function getPlotElement(graphId) {
        const root = document.getElementById(graphId);
        if (!root) {
            return null;
        }

        if (
            root.classList.contains("js-plotly-plot") ||
            root.classList.contains("plotly-graph-div")
        ) {
            return root;
        }

        return root.querySelector(".js-plotly-plot, .plotly-graph-div");
    }

    function buildExportTitle(layout) {
        const meta = (layout && layout.meta) || {};
        const title = meta.export_title || "";
        const subtitle = meta.export_subtitle || "";

        if (!title && !subtitle) {
            return layout && layout.title ? layout.title.text : "";
        }

        if (!subtitle) {
            return `<span style="font-size:${EXPORT_TITLE_FONT_SIZE}px"><b>${escapeHtml(title)}</b></span>`;
        }

        return (
            `<span style="font-size:${EXPORT_TITLE_FONT_SIZE}px"><b>${escapeHtml(title)}</b></span><br>` +
            `<span style="font-size:${EXPORT_SUBTITLE_FONT_SIZE}px"><sub>${escapeHtml(subtitle)}</sub></span>`
        );
    }

    async function downloadFromTempPlot(plot, options) {
        const exportData = JSON.parse(JSON.stringify(plot.data || []));
        const exportLayout = JSON.parse(JSON.stringify(plot.layout || {}));
        const exportConfig = {
            displayModeBar: false,
            responsive: false,
            staticPlot: true,
        };

        exportLayout.width = options.width;
        exportLayout.height = options.height;
        exportLayout.autosize = false;
        exportLayout.title = exportLayout.title || {};
        exportLayout.title.text = buildExportTitle(exportLayout);
        exportLayout.title.x = exportLayout.title.x ?? 0.5;
        exportLayout.title.xanchor = exportLayout.title.xanchor || "center";

        const tempContainer = document.createElement("div");
        tempContainer.style.position = "fixed";
        tempContainer.style.left = "-10000px";
        tempContainer.style.top = "0";
        tempContainer.style.width = `${options.width}px`;
        tempContainer.style.height = `${options.height}px`;
        document.body.appendChild(tempContainer);

        try {
            await window.Plotly.newPlot(tempContainer, exportData, exportLayout, exportConfig);
            await window.Plotly.downloadImage(tempContainer, options);
            await window.Plotly.purge(tempContainer);
        } finally {
            tempContainer.remove();
        }
    }

    async function handleDownload(button) {
        const graphId = button.dataset.graphId;
        const width = Number(button.dataset.exportWidth || 1600);
        const height = Number(button.dataset.exportHeight || 900);
        const plot = getPlotElement(graphId);

        if (!plot || !window.Plotly || typeof window.Plotly.downloadImage !== "function") {
            return;
        }

        const configuredName = button.dataset.filename;
        const titleText =
            plot.layout &&
            plot.layout.title &&
            typeof plot.layout.title.text === "string"
                ? plot.layout.title.text
                : "";
        const filename = sanitizeFilename(configuredName || titleText || graphId);

        await downloadFromTempPlot(plot, {
            format: "png",
            filename,
            width,
            height,
            scale: EXPORT_SCALE,
        });
    }

    document.addEventListener("click", function (event) {
        const button = event.target.closest(".plot-download-button");
        if (!button) {
            return;
        }

        event.preventDefault();
        handleDownload(button);
    });
})();
