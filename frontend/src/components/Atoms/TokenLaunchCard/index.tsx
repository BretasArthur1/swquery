import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  Twitter,
  Monitor,
  PiggyBank,
  CircleDollarSign,
  ChartCandlestick,
  Activity,
  Clock,
} from "lucide-react";

interface Launch {
  name: string;
  mint: string;
  symbol?: string;
  uri?: string;
  pool?: string;
  initialBuy: number;
  vTokensInBondingCurve: number;
  vSolInBondingCurve: number;
  marketCapSol: number;
  timestamp: number;
}

interface TokenDetails {
  name: string;
  symbol: string;
  description: string;
  image: string;
  twitter: string;
  website: string;
}

interface TokenLaunchCardProps {
  launch: Launch;
}

export default function TokenLaunchCard({ launch }: TokenLaunchCardProps) {
  const [details, setDetails] = useState<TokenDetails | null>(null);
  const [liveData, setLiveData] = useState(launch);

  useEffect(() => {
    // 🔴 Conectar ao WebSocket para receber dados em tempo real
    const ws = new WebSocket("wss://pumpportal.fun/api/data");

    ws.onopen = () => console.log("🔗 WebSocket conectado!");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      // Atualiza os dados apenas se o mint corresponder ao card atual
      if (data.mint === launch.mint) {
        setLiveData(data);
      }
    };

    ws.onerror = (error) => console.error("⚠️ Erro no WebSocket:", error);
    ws.onclose = () => console.log("🔌 Conexão WebSocket fechada.");

    return () => {
      ws.close();
    };
  }, [launch.mint]);

  useEffect(() => {
    if (launch.uri) {
      fetch(launch.uri)
        .then((response) => response.json())
        .then((data) => {
          setDetails({
            name: data.name || launch.name,
            symbol: data.symbol || launch.symbol || "N/A",
            description: data.description || "No description available",
            image: data.image || "",
            twitter: data.twitter || "",
            website: data.website || "",
          });
        })
        .catch((error) => console.error("❌ Falha ao buscar detalhes do token:", error));
    }
  }, [launch.uri, launch.name, launch.symbol]);

  return (
    <motion.div
      initial={{ scale: 0.9, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.3 }}
      className="bg-gray-800 rounded-lg p-6 shadow-lg flex gap-6 mb-6"
    >
      {/* 📌 Coluna 1: Imagem */}
      <div className="flex-shrink-0 w-2/9 flex items-center justify-center">
        {details?.image ? (
          <img
            src={details.image}
            alt={details.name}
            className="w-20 h-20 md:w-24 md:h-24 rounded-full object-cover"
          />
        ) : (
          <div className="w-20 h-20 md:w-24 md:h-24 rounded-full bg-gray-600 flex items-center justify-center text-white">
            No Image
          </div>
        )}
      </div>

      {/* 📌 Coluna 2: Dados Gerais e Detalhes */}
      <div className="flex-1">
        <h3 className="text-2xl font-bold mb-2">{details?.name || launch.name}</h3>
        <p className="text-sm text-gray-400 mb-2">Pool: {launch.pool || "Unknown"}</p>
        <p className="text-sm text-gray-400 mb-4">Mint: {launch.mint}</p>
        <p className="text-base text-gray-300 mb-4">{details?.description}</p>

        {/* 🔗 Links */}
        <div className="flex items-center gap-4">
          {details?.twitter && (
            <a
              href={details.twitter}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-blue-400"
            >
              <Twitter className="w-5 h-5" />
              Twitter
            </a>
          )}
          {details?.website && (
            <a
              href={details.website}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-blue-400"
            >
              <Monitor className="w-5 h-5" />
              Website
            </a>
          )}
        </div>
      </div>

      {/* 📌 Coluna 3: Dados Principais */}
      <div className="flex-1 grid grid-cols-1 gap-y-4">
        <p className="text-base flex items-center gap-2">
          <PiggyBank className="text-purple-500" />
          <span className="font-bold">Initial Buy:</span> {liveData.initialBuy.toFixed(2)}
        </p>
        <p className="text-base flex items-center gap-2">
          <CircleDollarSign className="text-purple-500" />
          <span className="font-bold">Market Cap:</span> {liveData.marketCapSol.toFixed(2)} SOL
        </p>
        <p className="text-base flex items-center gap-2">
          <ChartCandlestick className="text-purple-500" />
          <span className="font-bold">Tokens in Bonding Curve:</span>{" "}
          {liveData.vTokensInBondingCurve.toFixed(2)}
        </p>
        <p className="text-base flex items-center gap-2">
          <Activity className="text-purple-500" />
          <span className="font-bold">SOL in Bonding Curve:</span> {liveData.vSolInBondingCurve.toFixed(2)}
        </p>
        <p className="text-base flex items-center gap-2">
          <Clock className="text-purple-500" />
          <span className="font-bold">Last Update:</span>{" "}
          {new Date(liveData.timestamp).toLocaleString()}
        </p>
      </div>
    </motion.div>
  );
}