import { set } from 'date-fns';
import { useEffect, useState } from 'react';

const TrainAnnouncement = ({
  trainNumber,
  stationShortCode,
  arrivalDepartureTime,
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [audioQueue, setAudioQueue] = useState([]);
  const [usedAudioUrls, setUsedAudioUrls] = useState([]); // Keep track of played audio URLs so they are not played again

  const playAudio = async (audioUrl) => {
    if (usedAudioUrls.includes(audioUrl)) {
      return;
    }
    setIsPlaying(true);
    console.log('Playing audio:', audioUrl);
    try {
      const audio = new Audio(audioUrl);
      audio.onended = () => {
        setIsPlaying(false);
      };
      audio.play();
    } catch (error) {
      console.error('Error playing audio:', error);
    }
    setUsedAudioUrls((prevUrls) => [...prevUrls, audioUrl]);
    setAudioQueue((prevQueue) => prevQueue.slice(1));
  };

  const checkTrain = () => {
    console.log('Checking train every minute');

    const timeNow = new Date();
    timeNow.setHours(timeNow.getHours() + 3);
    const timeDifference = new Date(arrivalDepartureTime) - timeNow;
    if (timeDifference <= 300000) {
      const audioUrl = `https://junakuulutus.onrender.com/single-announcement/${arrivalDepartureTime}/${trainNumber}/${stationShortCode}`;
      if (!audioQueue.includes(audioUrl) && !usedAudioUrls.includes(audioUrl)) {
        setAudioQueue((prevQueue) => [...prevQueue, audioUrl]);
      }
    }
  };

  useEffect(() => {
    checkTrain();
    // Cleanup function to stop audio when component unmounts
    return () => {
      setIsPlaying(false); // Stop audio playback
    };
  }, []);

  useEffect(() => {
    if (audioQueue.length > 0 && !isPlaying) {
      playAudio(audioQueue[0]);
    }
  }, [audioQueue, isPlaying]);

  useEffect(() => {
    const interval = setInterval(checkTrain, 60000);
    return () => clearInterval(interval);
  }, []);

  return null;
};

export default TrainAnnouncement;
