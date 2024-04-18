CREATE DATABASE hiline_tool_database;
USE hiline_tool_database;
CREATE TABLE hiline_tool_database.Drawer (
    DrawerID INT AUTO_INCREMENT PRIMARY KEY,
    DrawerNum INT,
    DrawerBoxNum INT,
    DrawerStartX INT,
    DrawerStartY INT,
    DrawerPixelWidth INT,
    DrawerPixelHeight INT,
    DrawerYAML VARCHAR(255),
    DrawerPicAllTools VARCHAR(255),
    DrawerPicNoTools VARCHAR(255),
    DrawerSymbols JSON
);

CREATE TABLE hiline_tool_database.Tools (
    ToolID INT AUTO_INCREMENT PRIMARY KEY,
    ToolName VARCHAR(255),
    ToolType VARCHAR(255),
    ToolClassifierType VARCHAR(255),
    ToolDrawerID INT,
    ToolSymbolAvailable BOOLEAN,
    ToolSymbolPath VARCHAR(255),
    ToolCheckedOut BOOLEAN,
    ToolStartX INT,
    ToolStartY INT,
    ToolPixelWidth INT,
    ToolPixelHeight INT,
    ToolPictureWithPath VARCHAR(255),
    ToolPictureWithoutPath VARCHAR(255),
    ToolInfoTakenManually BOOLEAN,
    FOREIGN KEY (ToolDrawerID) REFERENCES hiline_tool_database.Drawer(DrawerID)
);

CREATE TABLE hiline_tool_database.Events (
    EventID INT AUTO_INCREMENT PRIMARY KEY,
    EventType INT,
    EventToolID INT,
    EventTimestamp TIMESTAMP,
    EventDrawerLocation INT,
    EventUserID INT,
    EventNotes VARCHAR(255),
    FOREIGN KEY (EventToolID) REFERENCES hiline_tool_database.Tools(ToolID),
    FOREIGN KEY (EventDrawerLocation) REFERENCES hiline_tool_database.Drawer(DrawerID)
);
