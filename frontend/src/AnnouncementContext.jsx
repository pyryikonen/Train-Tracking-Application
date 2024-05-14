import React, { createContext, useState } from 'react';

// Creating a new context for announcement queue
export const AnnouncementContext = createContext();

// AnnouncementProvider component responsible for providing announcement queue context to its children
export const AnnouncementProvider = ({ children }) => {
  // State to manage announcement queue
  const [queue, setQueue] = useState([]);

  return (
    // Providing announcement queue context to children components
    <AnnouncementContext.Provider value={{ queue, setQueue }}>
      {children}
    </AnnouncementContext.Provider>
  );
};
