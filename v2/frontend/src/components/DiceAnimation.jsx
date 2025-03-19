import React, { useState, useEffect, useRef } from 'react';
import { Box } from '@mui/material';

// Create dice faces as SVG elements
const DICE_FACES = [
  // Face 1
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" key="face1">
    <rect width="100" height="100" rx="15" fill="white" stroke="#ccc" strokeWidth="5" />
    <circle cx="50" cy="50" r="10" fill="#333" />
  </svg>,
  // Face 2
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" key="face2">
    <rect width="100" height="100" rx="15" fill="white" stroke="#ccc" strokeWidth="5" />
    <circle cx="25" cy="25" r="10" fill="#333" />
    <circle cx="75" cy="75" r="10" fill="#333" />
  </svg>,
  // Face 3
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" key="face3">
    <rect width="100" height="100" rx="15" fill="white" stroke="#ccc" strokeWidth="5" />
    <circle cx="25" cy="25" r="10" fill="#333" />
    <circle cx="50" cy="50" r="10" fill="#333" />
    <circle cx="75" cy="75" r="10" fill="#333" />
  </svg>,
  // Face 4
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" key="face4">
    <rect width="100" height="100" rx="15" fill="white" stroke="#ccc" strokeWidth="5" />
    <circle cx="25" cy="25" r="10" fill="#333" />
    <circle cx="25" cy="75" r="10" fill="#333" />
    <circle cx="75" cy="25" r="10" fill="#333" />
    <circle cx="75" cy="75" r="10" fill="#333" />
  </svg>,
  // Face 5
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" key="face5">
    <rect width="100" height="100" rx="15" fill="white" stroke="#ccc" strokeWidth="5" />
    <circle cx="25" cy="25" r="10" fill="#333" />
    <circle cx="25" cy="75" r="10" fill="#333" />
    <circle cx="50" cy="50" r="10" fill="#333" />
    <circle cx="75" cy="25" r="10" fill="#333" />
    <circle cx="75" cy="75" r="10" fill="#333" />
  </svg>,
  // Face 6
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" key="face6">
    <rect width="100" height="100" rx="15" fill="white" stroke="#ccc" strokeWidth="5" />
    <circle cx="25" cy="25" r="10" fill="#333" />
    <circle cx="25" cy="50" r="10" fill="#333" />
    <circle cx="25" cy="75" r="10" fill="#333" />
    <circle cx="75" cy="25" r="10" fill="#333" />
    <circle cx="75" cy="50" r="10" fill="#333" />
    <circle cx="75" cy="75" r="10" fill="#333" />
  </svg>
];

// Single dice component that handles animation
const SingleDice = ({ value, rolling, size = 70 }) => {
  const [currentFace, setCurrentFace] = useState(0);
  const intervalRef = useRef(null);
  const timeoutRef = useRef(null);
  
  // Reset and start animation when rolling prop changes
  useEffect(() => {
    // Clear any existing timers
    if (intervalRef.current) clearInterval(intervalRef.current);
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    
    if (rolling) {
      // Start with a random face
      setCurrentFace(Math.floor(Math.random() * 6));
      
      // Create animation interval
      intervalRef.current = setInterval(() => {
        setCurrentFace(Math.floor(Math.random() * 6));
      }, 100);
      
      // Stop animation after 1.5 seconds and show final value
      timeoutRef.current = setTimeout(() => {
        clearInterval(intervalRef.current);
        // Subtract 1 because array is 0-indexed but dice values are 1-6
        setCurrentFace(value - 1);
      }, 1500);
    } else {
      // If not rolling, show the actual value (or default to first face)
      setCurrentFace(value ? value - 1 : 0);
    }
    
    // Cleanup function
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, [rolling, value]);
  
  return (
    <Box
      sx={{
        width: `${size}px`,
        height: `${size}px`,
        transition: rolling ? 'transform 0.1s ease' : 'transform 0.3s ease-out',
        transform: rolling ? `rotate(${Math.random() * 360}deg) translateY(${Math.random() * 10}px)` : 'rotate(0deg)',
        animation: rolling ? 'shake 0.5s infinite' : 'none',
        '@keyframes shake': {
          '0%': { transform: 'rotate(0deg)' },
          '25%': { transform: 'rotate(10deg) translateY(5px)' },
          '50%': { transform: 'rotate(0deg) translateY(-5px)' },
          '75%': { transform: 'rotate(-10deg) translateY(5px)' },
          '100%': { transform: 'rotate(0deg)' }
        }
      }}
    >
      {DICE_FACES[currentFace]}
    </Box>
  );
};

// Main dice animation component
const DiceAnimation = ({ dice1, dice2, rolling, onRollEnd }) => {
  // Set a timeout to call onRollEnd after animation completes
  useEffect(() => {
    let timer;
    if (rolling && onRollEnd) {
      timer = setTimeout(() => {
        onRollEnd();
      }, 1800); // Slightly longer than the dice animation to ensure it completes
    }
    return () => {
      if (timer) clearTimeout(timer);
    };
  }, [rolling, onRollEnd]);

  return (
    <Box 
      sx={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        gap: 3,
        mb: 3,
        mt: 3,
        minHeight: '80px',
        perspective: '1000px'
      }}
    >
      <SingleDice value={dice1} rolling={rolling} />
      <SingleDice value={dice2} rolling={rolling} />
    </Box>
  );
};

export default DiceAnimation;
