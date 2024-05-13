import React, { createContext, useState } from 'react';

export const AnnouncementContext = createContext();

export const AnnouncementProvider = ({ children }) => {
  const [queue, setQueue] = useState([]);

  return (
    <AnnouncementContext.Provider value={{ queue, setQueue }}>
      {children}
    </AnnouncementContext.Provider>
  );
};
