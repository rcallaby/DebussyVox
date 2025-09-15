import React, { useEffect, useRef } from "react";

/**
 * Simple canvas avatar that exposes:
 * - recordAndSend(sendCallback)
 * - speak(audioUrl) -> plays audio while animating mouth
 *
 * We'll export functions via a ref on the component instance.
 */
const Avatar = React.forwardRef((props, ref) => {
  const canvasRef = useRef(null);
  const audioRef = useRef(null);
  const animationRef = useRef(null);

  useEffect(() => {
    const c = canvasRef.current;
    c.width = 280;
    c.height = 280;
    drawFace(0);
    // expose speak function to parent via ref
    if (ref) ref.current = { speak };
  }, []);

  function drawFace(mouthOpen = 0) {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // face
    ctx.fillStyle = "#fdebd0";
    ctx.beginPath();
    ctx.arc(140, 110, 80, 0, Math.PI * 2);
    ctx.fill();

    // eyes
    ctx.fillStyle = "#111";
    ctx.beginPath();
    ctx.arc(115, 95, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(165, 95, 8, 0, Math.PI * 2);
    ctx.fill();

    // mouth
    ctx.fillStyle = "#7b2a2a";
    const h = 6 + mouthOpen * 26;
    ctx.beginPath();
    ctx.ellipse(140, 160, 36, h, 0, 0, Math.PI * 2);
    ctx.fill();
  }

  // Play audio and animate mouth
  async function speak(audioUrl) {
    // stop current if playing
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }
    const audio = new Audio(audioUrl);
    audioRef.current = audio;

    audio.onplay = () => {
      let t = 0;
      const step = () => {
        // simple mouth oscillation proportional to playback position
        const progress = audio.currentTime / Math.max(0.001, audio.duration);
        const mouthOpen = 0.2 + Math.abs(Math.sin(t)) * (0.7 * (1 - Math.abs(0.5 - progress) * 2));
        drawFace(mouthOpen);
        t += 0.12;
        animationRef.current = requestAnimationFrame(step);
      };
      animationRef.current = requestAnimationFrame(step);
    };

    audio.onended = () => {
      if (animationRef.current) cancelAnimationFrame(animationRef.current);
      drawFace(0);
    };

    audio.play().catch(e => console.error("Audio play failed", e));
  }

  // Expose a recording function that uses MediaRecorder — parent will pass a callback
  const startRecording = async (onAudioReady) => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const mediaRecorder = new MediaRecorder(stream);
    const chunks = [];
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.push(e.data);
    };
    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: "audio/webm" });
      onAudioReady(blob);
      stream.getTracks().forEach(t => t.stop());
    };
    mediaRecorder.start();
    return mediaRecorder;
  };

  return (
    <div style={{display:"flex", gap:16, alignItems:"center"}}>
      <canvas ref={canvasRef} style={{borderRadius:12, background:"#e8f4ff"}} />
      <div style={{display:"flex", flexDirection:"column"}}>
        <small>Avatar</small>
      </div>
      {/* expose startRecording via props? Parent will call startRecording via ref */}
      <div style={{display:"none"}} />
    </div>
  );
});

export default Avatar;
