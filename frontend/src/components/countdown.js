import React, { useState, useEffect } from "react";
import styled from "@emotion/styled";

function Countdown() {
  const [timeLeft, setTimeLeft] = useState(0);
  const [state, setState] = useState(0);

  useEffect(() => {
    const fetchTimeLeft = async () => {
      try {
        const response = await fetch("http://127.0.0.1:5000/time_left", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (response.ok) {
          const data = await response.json();
          setTimeLeft(Math.floor(data.time_left));
          setState(data.state);
          console.log(state);
        } else {
          console.log("Server returned an error");
        }
      } catch (error) {
        console.log("Fetch error: ", error);
      }
    };

    fetchTimeLeft();

    const intervalId = setInterval(fetchTimeLeft, 100);

    return () => {
      clearInterval(intervalId);
    };
  }, []);

  const controlTimer = async (action) => {
    await fetch("http://127.0.0.1:5000/control", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ action }),
    });
  };

  useEffect(() => {
    const resetTimer = async () => {
      await fetch("http://127.0.0.1:5000/reset", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });
    };

    resetTimer();
  }, []);

  const minutes = String(Math.floor(timeLeft / 60)).padStart(2, "0");
  const seconds = String(timeLeft % 60).padStart(2, "0");

  return (
    <Container>
      <CountdownBox>
        <h1>
          {minutes}:{seconds}
        </h1>
      </CountdownBox>
      {state === 0 && (
        <button onClick={() => controlTimer("start")}>Start</button>
      )}
      {(state === 2 || state === 4) && (
        <button onClick={() => controlTimer("resume")}>Resume</button>
      )}
      {(state === 1 || state === 3) && (
        <button onClick={() => controlTimer("pause")}>Pause</button>
      )}
    </Container>
  );
}

const Container = styled.div`
  width: 100%;
  padding: 40px 16vw;
  display
`;

const CountdownBox = styled.div`
  width: 100%;
  display: flex;
`;

export default Countdown;