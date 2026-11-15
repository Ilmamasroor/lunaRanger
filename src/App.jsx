import React, { useCallback, useState } from 'react';
import Header from './components/Header';
import Starfield from './components/Starfield';
import MainMenu from './screens/MainMenu';
import MissionGuide from './screens/MissionGuide';
import MissionMapScreen from './screens/MissionMapScreen';
import DayGoalModal from './screens/DayGoalModal';
import Gameplay from './screens/Gameplay';
import DayCompleteModal from './screens/DayCompleteModal';
import MissionDebrief from './screens/MissionDebrief';
import { MISSION_DAYS } from './data/missionConfig';

export default function App() {
  // Navigation State Machine:
  // 'mainMenu' -> 'missionGuide' -> 'trailMap' -> 'dayGoal' -> 'gameplay' -> 'dayComplete' -> 'trailMap' (or 'debrief')
  const [currentScreen, setCurrentScreen] = useState('mainMenu'); 
  const [cadetName, setCadetName] = useState('Cadet Muneeba');
  const [avatar, setAvatar] = useState('👩‍🚀');
  const [dayIndex, setDayIndex] = useState(0); // 0 = Day 1
  const [gameStarted, setGameStarted] = useState(false);
  const completeDay = useCallback(() => setCurrentScreen('dayComplete'), []);
  const goHome = () => {
    setCurrentScreen('mainMenu');
    setDayIndex(0);
    setGameStarted(false);
  };

  const currentDayData = MISSION_DAYS[dayIndex] || MISSION_DAYS[0];

  return (
    <div className="min-h-screen flex flex-col justify-between relative selection:bg-cyan-500 selection:text-black">
      {/* Animated Twinkling Starfield Canvas */}
      <Starfield />

      {/* Top Header with New Transparent Rocket Favicon & Logo */}
      <Header
        cadetName={cadetName}
        avatar={avatar}
        onHomeClick={goHome}
      />

      {/* Main Screens Container */}
      <main className="flex-1 flex flex-col items-center justify-center p-4 relative z-10">
        {currentScreen === 'mainMenu' && (
          <MainMenu
            cadetName={cadetName}
            setCadetName={setCadetName}
            avatar={avatar}
            setAvatar={setAvatar}
            onStartMission={() => setCurrentScreen('missionGuide')}
          />
        )}

        {currentScreen === 'missionGuide' && (
          <MissionGuide
            onContinue={() => setCurrentScreen('trailMap')}
            onBack={() => setCurrentScreen('mainMenu')}
          />
        )}

        {/* The New Curly/Snake Trail Map Screen */}
        {currentScreen === 'trailMap' && (
          <MissionMapScreen
            currentDayIndex={dayIndex}
            onSelectDay={(selectedDayIdx) => {
              if (selectedDayIdx === dayIndex) setCurrentScreen('dayGoal');
            }}
            onBackToHome={goHome}
          />
        )}

        {currentScreen === 'dayGoal' && (
          <DayGoalModal
            dayData={currentDayData}
            onStartDay={() => {
              setGameStarted(true);
              setCurrentScreen('gameplay');
            }}
            onBack={() => setCurrentScreen('trailMap')}
          />
        )}

        {gameStarted && (
          <Gameplay
            active={currentScreen === 'gameplay'}
            dayData={currentDayData}
            onCompleteDay={completeDay}
          />
        )}

        {currentScreen === 'dayComplete' && (
          <DayCompleteModal
            dayData={currentDayData}
            onContinueToMap={() => {
              const nextDay = dayIndex + 1;
              if (nextDay < MISSION_DAYS.length) {
                setDayIndex(nextDay);
                setCurrentScreen('trailMap'); // Rocket will animate smoothly to next node!
              } else {
                setCurrentScreen('debrief');
              }
            }}
          />
        )}

        {currentScreen === 'debrief' && (
          <MissionDebrief
            onBackToMainMenu={goHome}
          />
        )}
      </main>

      {/* Clean Footer */}
      <footer className="relative z-10 px-4 py-2 text-center text-[10px] text-cyan-400/70 font-semibold border-t border-cyan-900/30">
        NASA Space Apps Challenge 2026 • Team Neural Knights
      </footer>
    </div>
  );
}
