import { BrowserRouter, Routes, Route, useLocation } from 'react-router-dom';
import Header from './components/Header';
import GlobalChat from './components/GlobalChat';
import { ThemeProvider } from './contexts/ThemeContext';
import Dashboard from './pages/Dashboard';
import Learn from './pages/Learn';
import PracticeV2 from './pages/PracticeV2';
import Formulas from './pages/Formulas';
import Settings from './pages/Settings';
import Course from './pages/Course';
import './styles/global.css';

// Inner component so useLocation works inside BrowserRouter
function AppRoutes() {
  const location = useLocation();
  // Don't show global chat on pages that have their own contextual chat
  const showGlobalChat = location.pathname !== '/learn'
    && !location.pathname.startsWith('/learn/')
    && location.pathname !== '/practice';

  return (
    <>
      <Header />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/learn" element={<Learn />} />
        <Route path="/learn/:topicId" element={<Learn />} />
        <Route path="/practice" element={<PracticeV2 />} />
        <Route path="/formulas" element={<Formulas />} />
        <Route path="/course" element={<Course />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
      {showGlobalChat && <GlobalChat />}
    </>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </ThemeProvider>
  );
}
