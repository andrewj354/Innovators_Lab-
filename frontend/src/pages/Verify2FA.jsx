import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/Verify2FA.css";

export default function Verify2FA() {
  const navigate = useNavigate();
  const inputsRef = useRef([]);
  const [otp, setOtp] = useState(["", "", "", "", "", ""]);
  const [secondsLeft, setSecondsLeft] = useState(300);
  const [canResend, setCanResend] = useState(false);

  useEffect(() => {
    if (secondsLeft === 0) {
      setCanResend(true);
      return;
    }

    const timer = setInterval(() => {
      setSecondsLeft((prev) => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [secondsLeft]);

  const formatTime = (seconds) => {
    const min = String(Math.floor(seconds / 60)).padStart(2, "0");
    const sec = String(seconds % 60).padStart(2, "0");
    return `${min}:${sec}`;
  };

  const handleChange = (value, index) => {
    if (!/^\d?$/.test(value)) return;

    const next = [...otp];
    next[index] = value;
    setOtp(next);

    if (value && index < 5) {
      inputsRef.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (e, index) => {
    if (e.key === "Backspace" && !otp[index] && index > 0) {
      inputsRef.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e) => {
    e.preventDefault();
    const pasted = e.clipboardData.getData("text").replace(/\D/g, "").slice(0, 6);
    if (!pasted) return;

    const next = ["", "", "", "", "", ""];
    pasted.split("").forEach((digit, index) => {
      next[index] = digit;
    });

    setOtp(next);
    inputsRef.current[Math.min(pasted.length, 5)]?.focus();
  };

  const handleVerify = () => {
    const code = otp.join("");
    if (code.length !== 6) return;

    console.log("OTP code:", code);
  };

  const handleResend = () => {
    setOtp(["", "", "", "", "", ""]);
    setSecondsLeft(300);
    setCanResend(false);
    inputsRef.current[0]?.focus();
    console.log("Resend OTP");
  };

  return (
    <div className="verify-page">
      <div className="verify-card">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ←
        </button>

        <div className="verify-logo">INNOVATORS LAB</div>

        <h1 className="verify-title">OTP Verification</h1>
        <p className="verify-text">
          We will send you a one time password to your email address
        </p>
        <p className="verify-email">software_nure@gmail.com</p>

        <div className="otp-row">
          {otp.map((digit, index) => (
            <input
              key={index}
              ref={(el) => (inputsRef.current[index] = el)}
              className="otp-input"
              type="text"
              inputMode="numeric"
              maxLength={1}
              value={digit}
              onChange={(e) => handleChange(e.target.value, index)}
              onKeyDown={(e) => handleKeyDown(e, index)}
              onPaste={index === 0 ? handlePaste : undefined}
            />
          ))}
        </div>

        <div className="timer">{formatTime(secondsLeft)}</div>

        <div className="resend-line">
          Didn't you receive the OTP?{" "}
          <button
            type="button"
            className="resend-btn"
            onClick={handleResend}
            disabled={!canResend}
          >
            Надіслати код повторно
          </button>
        </div>

        <button className="verify-btn" onClick={handleVerify}>
          Verify
        </button>
      </div>
    </div>
  );
}