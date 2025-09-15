// simple api helpers
export async function uploadAudio(blob) {
  const form = new FormData();
  form.append("audio", blob, "voice.webm");
  const res = await fetch("/voice", { method: "POST", body: form });
  if (!res.ok) {
    const txt = await res.text();
    throw new Error("upload failed: " + txt);
  }
  return res.json(); // { text, reply, audio_url }
}
