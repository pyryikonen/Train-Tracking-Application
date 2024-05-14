import { useContext, useEffect, useRef, useState } from 'react';
import { AnnouncementContext } from './AnnouncementContext.jsx';

// AnnouncementPlayer component responsible for playing announcements
const AnnouncementPlayer = () => {
  // Accessing announcement queue and setter function from AnnouncementContext
  const { queue, setQueue } = useContext(AnnouncementContext);
  // State to track if an announcement is currently playing
  const [isPlaying, setIsPlaying] = useState(false);
  // Reference to the audio element
  const audioRef = useRef();

  useEffect(() => {
    // Effect to play announcements when the queue changes and no announcement is currently playing
    if (queue.length === 0 || isPlaying) return;

    // Get the URL of the next announcement from the queue
    const audioUrl = queue[0];
    // Remove the played announcement from the queue
    setQueue((prevQueue) => prevQueue.slice(1));

    // Set the audio source to the URL of the announcement
    audioRef.current.src = audioUrl;
    // Start playing the announcement
    setIsPlaying(true);
    // Play the audio and handle any errors
    audioRef.current.play().catch((error) => {
      console.log('Error playing announcement:', error);
      setIsPlaying(false);
    });
  }, [queue, isPlaying]);

  return (
    // Audio element for playing announcements
    <audio
      ref={audioRef} // Reference to the audio element
      onEnded={() => {
        // Callback function when the announcement ends
        setIsPlaying(false); // Update state to indicate that no announcement is currently playing
      }}
    />
  );
};

export default AnnouncementPlayer;
