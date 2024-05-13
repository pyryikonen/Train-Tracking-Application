import { useContext, useEffect, useRef, useState } from 'react';
import { AnnouncementContext } from './AnnouncementContext.jsx';

const AnnouncementPlayer = () => {
  const { queue, setQueue } = useContext(AnnouncementContext);
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef();

  useEffect(() => {
    if (queue.length === 0 || isPlaying) return;

    const audioUrl = queue[0];
    setQueue((prevQueue) => prevQueue.slice(1));

    audioRef.current.src = audioUrl;
    setIsPlaying(true);
    audioRef.current.play().catch((error) => {
      console.log('Error playing announcement:', error);
      setIsPlaying(false);
    });
  }, [queue, isPlaying]);

  return (
    <audio
      ref={audioRef}
      onEnded={() => {
        setIsPlaying(false);
      }}
    />
  );
};

export default AnnouncementPlayer;
