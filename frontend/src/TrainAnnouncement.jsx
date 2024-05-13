import { useEffect, useState, useRef, useContext } from 'react';
import { AnnouncementContext } from './AnnouncementContext';

const TrainAnnouncement = ({
  arrival,
  trainNumber,
  stationShortCode,
  arrivalDepartureTime,
}) => {
  const { queue, setQueue } = useContext(AnnouncementContext);
  const [usedAudioUrls, setUsedAudioUrls] = useState([]);

  useEffect(() => {
    console.log('TrainAnnouncement useEffect');
    const interval = setInterval(() => {
      const timeNow = new Date();
      timeNow.setHours(timeNow.getHours() + 3);
      const timeDifference = new Date(arrivalDepartureTime) - timeNow;
      if (timeDifference <= 300000) {
        var audioUrl = '';
        if (arrival) {
          audioUrl = `https://junakuulutus.onrender.com/arrival-announcement/${arrivalDepartureTime}/${trainNumber}/${stationShortCode}`;
        } else {
          audioUrl = `https://junakuulutus.onrender.com/departure-announcement/${arrivalDepartureTime}/${trainNumber}/${stationShortCode}`;
        }
        if (!queue.includes(audioUrl) && !usedAudioUrls.includes(audioUrl)) {
          setQueue((prevQueue) => [...prevQueue, audioUrl]);
        }
      }
    }, 30000);
    console.log('TrainAnnouncement useEffect end');
    return () => clearInterval(interval);
  }, []);

  return null;
};

export default TrainAnnouncement;
