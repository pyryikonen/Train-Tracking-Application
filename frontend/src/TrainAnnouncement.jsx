import { useEffect, useState, useRef, useContext } from 'react';
import { AnnouncementContext } from './AnnouncementContext';

// TrainAnnouncement component responsible for managing train announcements
const TrainAnnouncement = ({
  arrival,
  trainNumber,
  stationShortCode,
  arrivalDepartureTime,
}) => {
  // Accessing announcement queue and setter function from AnnouncementContext
  const { queue, setQueue } = useContext(AnnouncementContext);
  // State to keep track of used audio URLs
  const [usedAudioUrls, setUsedAudioUrls] = useState([]);

  useEffect(() => {
    // Function to run when component mounts and on every update
    console.log('TrainAnnouncement useEffect');
    // Setting up interval to check for upcoming train announcements
    const interval = setInterval(() => {
      // Getting current time and adjusting to local time (GMT+3 in this case)
      const timeNow = new Date();
      timeNow.setHours(timeNow.getHours() + 3);
      // Calculating time difference between current time and announcement time
      const timeDifference = new Date(arrivalDepartureTime) - timeNow;
      // Checking if the announcement time is within 5 minutes
      if (timeDifference <= 300000) {
        var audioUrl = '';
        // Constructing audio URL based on arrival/departure and parameters
        if (arrival) {
          audioUrl = `https://junakuulutus.onrender.com/arrival-announcement/${arrivalDepartureTime}/${trainNumber}/${stationShortCode}`;
        } else {
          audioUrl = `https://junakuulutus.onrender.com/departure-announcement/${arrivalDepartureTime}/${trainNumber}/${stationShortCode}`;
        }
        // Checking if the audio URL is not already in the queue or played already
        if (!queue.includes(audioUrl) && !usedAudioUrls.includes(audioUrl)) {
          // Adding the audio URL to the announcement queue
          setQueue((prevQueue) => [...prevQueue, audioUrl]);
        }
      }
    }, 30000); // Interval set to check every 30 seconds
    console.log('TrainAnnouncement useEffect end');
    // Cleanup function to clear interval when component unmounts
    return () => clearInterval(interval);
  }, []); // Empty dependency array ensures useEffect runs only once on mount

  // Returning null because TrainAnnouncement component doesn't render anything
  return null;
};

export default TrainAnnouncement;
