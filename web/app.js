const status = document.querySelector("#worker-status");
const statusText = document.querySelector("#worker-status-text");
const workerRetry = document.querySelector("#worker-retry");
const fileInput = document.querySelector("#video-file");
const pickerTitle = document.querySelector(".picker-title");
const sourceDetails = document.querySelector("#source-details");
const preview = document.querySelector("#source-preview");
const fileName = document.querySelector("#file-name");
const fileDuration = document.querySelector("#file-duration");
const previewError = document.querySelector("#preview-error");
let previewUrl;
let selectedFile;

async function connectWorker() {
  workerRetry.hidden = true;
  status.dataset.state = "checking";
  statusText.textContent = "Checking local worker…";
  try {
    const response = await fetch("/api/v1/health", { cache: "no-store" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const health = await response.json();
    if (health.protocol_version !== 1 || health.status !== "ready") {
      throw new Error("Unsupported worker protocol");
    }
    status.dataset.state = "ready";
    statusText.textContent = `Local worker ready · v${health.protocol_version}`;
  } catch {
    status.dataset.state = "error";
    statusText.textContent = "Local worker unavailable";
    workerRetry.hidden = false;
  }
}

workerRetry.addEventListener("click", connectWorker);

function formatDuration(seconds) {
  if (!Number.isFinite(seconds)) return "Duration unavailable";
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const remainingSeconds = Math.floor(seconds % 60);
  if (hours) return `${String(hours).padStart(2, "0")}:${String(minutes).padStart(2, "0")}:${String(remainingSeconds).padStart(2, "0")}`;
  return `${String(minutes).padStart(2, "0")}:${String(remainingSeconds).padStart(2, "0")}`;
}

fileInput.addEventListener("change", () => {
  const file = fileInput.files?.[0];
  if (!file) return;

  selectedFile = file;
  pickerTitle.textContent = "Choose a different video";
  previewError.hidden = true;
  previewError.textContent = "";
  preview.removeAttribute("src");
  if (previewUrl) URL.revokeObjectURL(previewUrl);
  previewUrl = URL.createObjectURL(file);
  preview.src = previewUrl;
  sourceDetails.hidden = false;
  fileName.textContent = file.name;
  fileDuration.textContent = "Reading duration…";
  timelineDuration.textContent = "Reading duration…";
  fileInput.value = "";
});

preview.addEventListener("loadedmetadata", () => {
  previewError.hidden = true;
  const duration = formatDuration(preview.duration);
  const resolution = preview.videoWidth && preview.videoHeight
    ? `${preview.videoWidth} × ${preview.videoHeight}`
    : "Resolution unavailable";
  fileDuration.textContent = `${duration} · ${resolution} · ${(selectedFile.size / (1024 * 1024)).toFixed(1)} MB`;
});

preview.addEventListener("error", () => {
  fileDuration.textContent = "Preview unavailable";
  previewError.textContent = "This video could not be previewed in your browser. Try another MP4, MOV, or MKV; some codecs may not be supported.";
  previewError.hidden = false;
});

window.addEventListener("beforeunload", () => {
  if (previewUrl) URL.revokeObjectURL(previewUrl);
});

connectWorker();
