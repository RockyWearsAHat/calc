// Local Account & Progression Manager (Simulated Backend)

const ACCOUNT_KEY = 'calc_mastery_account';

export function getAccount() {
  const data = localStorage.getItem(ACCOUNT_KEY);
  if (data) return JSON.parse(data);
  return {
    isLoggedIn: true,
    name: "Local Student",
    level: 1, // Overall calculus level
    canvasTokenSaved: false,
    topics: {} // topicId -> { mastery: 0.0 to 1.0, attempts: 0, correct: 0 }
  };
}

export function saveAccount(data) {
  localStorage.setItem(ACCOUNT_KEY, JSON.stringify(data));
}

export function login(name, linkCanvas = false) {
  const account = getAccount();
  account.isLoggedIn = true;
  account.name = name;
  if (linkCanvas) {
    account.canvasTokenSaved = true;
  }
  saveAccount(account);
  return account;
}

export function logout() {
  localStorage.removeItem(ACCOUNT_KEY);
  return getAccount();
}

/**
 * Updates a student's mastery in a specific topic
 */
export function updateMastery(topicId, isCorrect) {
  const account = getAccount();
  if (!account.topics[topicId]) {
    account.topics[topicId] = { mastery: 0.0, attempts: 0, correct: 0 };
  }
  
  const stats = account.topics[topicId];
  stats.attempts += 1;
  
  if (isCorrect) {
    stats.correct += 1;
    // Boost mastery quickly if starting out, slower as you approach 1.0
    stats.mastery = Math.min(1.0, stats.mastery + 0.15 * (1 - stats.mastery));
  } else {
    // Drop mastery slightly
    stats.mastery = Math.max(0.0, stats.mastery - 0.05);
  }

  // Level up overall 
  const totalConceptsMastered = Object.values(account.topics).filter(t => t.mastery >= 0.8).length;
  account.level = 1 + Math.floor(totalConceptsMastered / 3);

  saveAccount(account);
  return account;
}

/**
 * Returns diagnostic format for UI components
 */
export function getDiagnosticProgress() {
  const account = getAccount();
  return {
    topics: Object.entries(account.topics).map(([id, data]) => ({
      id,
      mastery: data.mastery
    }))
  };
}