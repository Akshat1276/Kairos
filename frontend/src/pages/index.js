import { useState, useEffect } from 'react';
import { Play, Square, RefreshCw, ExternalLink, Activity, DollarSign, Clock, Zap, X } from 'lucide-react';
import axios from 'axios';

export default function Home() {
  const [agentStatus, setAgentStatus] = useState({
    running: false,
    nextRun: '',
    timeUntilNext: 0,
    polygonBalance: '0',
    hederaBalance: '0',
    totalProfit: 0,
    recentTrades: [],
    logs: []
  });

  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    const interval = setInterval(fetchStatus, 5000);
    fetchStatus();
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const timer = setInterval(() => {
      if (agentStatus.timeUntilNext > 0) {
        setAgentStatus(prev => ({
          ...prev,
          timeUntilNext: prev.timeUntilNext - 1
        }));
      }
    }, 1000);
    return () => clearInterval(timer);
  }, [agentStatus.timeUntilNext]);

  useEffect(() => {
    if (notifications.length > 0) {
      const timer = setTimeout(() => {
        setNotifications(prev => prev.slice(1));
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [notifications]);

  const fetchStatus = async () => {
    try {
      const response = await axios.get('/api/status');
      setAgentStatus(response.data);
    } catch (error) {
      console.error('Failed to fetch status:', error);
    }
  };

  const startAgent = async () => {
    try {
      await axios.post('/api/start');
      setNotifications(prev => [...prev, { id: Date.now(), message: 'Kairos Agent Started Successfully' }]);
      fetchStatus();
    } catch (error) {
      console.error('Failed to start agent:', error);
      setNotifications(prev => [...prev, { id: Date.now(), message: 'Failed to start agent' }]);
    }
  };

  const stopAgent = async () => {
    try {
      await axios.post('/api/stop');
      setNotifications(prev => [...prev, { id: Date.now(), message: 'Kairos Agent Stopped' }]);
      fetchStatus();
    } catch (error) {
      console.error('Failed to stop agent:', error);
    }
  };

  const dismissNotification = (id) => {
    setNotifications(prev => prev.filter(notification => notification.id !== id));
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getTransactionUrl = (network, txHash) => {
    if (network === 'polygon') {
      return `https://amoy.polygonscan.com/tx/${txHash}`;
    } else if (network === 'hedera') {
      return `https://hashscan.io/testnet/transaction/${txHash}`;
    }
    return '#';
  };

  const getLogColor = (level) => {
    switch (level) {
      case 'error': return 'text-red-500';
      case 'warning': return 'text-yellow-500';
      case 'success': return 'text-green-500';
      default: return 'text-gray-300';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      <div className="bg-black/20 backdrop-blur-sm border-b border-white/10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Zap className="w-8 h-8 text-purple-400" />
              <h1 className="text-2xl font-bold">Kairos Agent</h1>
              
            </div>
            <div className="flex items-center space-x-4">
              <div className={`flex items-center space-x-2 ${agentStatus.running ? 'text-green-400' : 'text-red-400'}`}>
                <Activity className="w-5 h-5" />
                <span className="font-semibold">
                  {agentStatus.running ? 'ACTIVE' : 'INACTIVE'}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <RefreshCw className="w-5 h-5 mr-2" />
              Agent Control
            </h2>
            <div className="space-y-4">
              <button
                onClick={agentStatus.running ? stopAgent : startAgent}
                className={`w-full flex items-center justify-center space-x-2 px-4 py-3 rounded-lg font-semibold transition-colors ${
                  agentStatus.running 
                    ? 'bg-red-600 hover:bg-red-700 text-white' 
                    : 'bg-green-600 hover:bg-green-700 text-white'
                }`}
              >
                {agentStatus.running ? <Square className="w-5 h-5" /> : <Play className="w-5 h-5" />}
                <span>{agentStatus.running ? 'Stop Agent' : 'Start Agent'}</span>
              </button>
              
              {agentStatus.running && (
                <div className="bg-white/5 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm text-gray-300">Next execution in:</span>
                    <Clock className="w-4 h-4 text-gray-400" />
                  </div>
                  <div className="text-2xl font-mono text-purple-400">
                    {formatTime(agentStatus.timeUntilNext)}
                  </div>
                </div>
              )}
            </div>
          </div>

          <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <h2 className="text-xl font-semibold mb-4 flex items-center">
              <DollarSign className="w-5 h-5 mr-2" />
              Account Balances
            </h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Polygon (WETH)</span>
                <span className="font-semibold">{agentStatus.polygonBalance}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Hedera (HBAR)</span>
                <span className="font-semibold">{agentStatus.hederaBalance}</span>
              </div>
              <div className="border-t border-white/10 pt-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Total Profit</span>
                  <span className={`font-bold ${agentStatus.totalProfit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    {agentStatus.totalProfit >= 0 ? '+' : ''}{agentStatus.totalProfit.toFixed(4)} ETH
                  </span>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <h2 className="text-xl font-semibold mb-4">Network Status</h2>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-purple-500 rounded-full"></div>
                  <span>Polygon Amoy</span>
                </div>
                <span className="text-green-400 text-sm">Connected</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
                  <span>Hedera Testnet</span>
                </div>
                <span className="text-green-400 text-sm">Connected</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                  <span>1inch API</span>
                </div>
                <span className="text-green-400 text-sm">Active</span>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Trades and Logs */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Recent Trades */}
          <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <h2 className="text-xl font-semibold mb-4">Recent Trades</h2>
            <div className="space-y-3 max-h-96 overflow-y-auto">
              {agentStatus.recentTrades.length > 0 ? (
                agentStatus.recentTrades.map((trade) => (
                  <div key={trade.id} className="bg-white/5 rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex items-center space-x-2">
                        <div className={`w-3 h-3 rounded-full ${
                          trade.network === 'polygon' ? 'bg-purple-500' : 'bg-blue-500'
                        }`}></div>
                        <span className="capitalize font-semibold">{trade.network}</span>
                        <span className={`px-2 py-1 rounded text-xs ${
                          trade.status === 'confirmed' ? 'bg-green-600' :
                          trade.status === 'pending' ? 'bg-yellow-600' : 'bg-red-600'
                        }`}>
                          {trade.status}
                        </span>
                      </div>
                      <span className={`font-semibold ${trade.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                        {trade.profit >= 0 ? '+' : ''}{trade.profit.toFixed(4)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center text-sm text-gray-300">
                      <span>{trade.amount}</span>
                      <a
                        href={getTransactionUrl(trade.network, trade.txHash)}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center space-x-1 hover:text-purple-400 transition-colors"
                      >
                        <span>View Tx</span>
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center text-gray-400 py-8">
                  No recent trades
                </div>
              )}
            </div>
          </div>

          {/* Live Logs */}
          <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
            <h2 className="text-xl font-semibold mb-4">Live Logs</h2>
            <div className="bg-black/30 rounded-lg p-4 font-mono text-sm max-h-96 overflow-y-auto">
              {agentStatus.logs.length > 0 ? (
                agentStatus.logs.map((log, index) => (
                  <div key={index} className="mb-1">
                    <span className="text-gray-400">{log.timestamp}</span>
                    <span className={`ml-2 ${getLogColor(log.level)}`}>
                      [{log.level.toUpperCase()}]
                    </span>
                    <span className="ml-2">{log.message}</span>
                  </div>
                ))
              ) : (
                <div className="text-gray-400">No logs available</div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Notifications */}
      {notifications.length > 0 && (
        <div className="fixed top-4 right-4 space-y-2 z-50">
          {notifications.slice(-3).map((notification) => (
            <div
              key={notification.id}
              className="bg-purple-500/90 backdrop-blur-sm text-white px-4 py-2 rounded-lg shadow-lg flex items-center justify-between min-w-[280px]"
            >
              <span>{notification.message}</span>
              <button
                onClick={() => dismissNotification(notification.id)}
                className="ml-3 hover:bg-white/20 rounded-full p-1 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}