import { useEffect, useState } from 'react';

import type { PipecatBaseChildProps } from '@pipecat-ai/voice-ui-kit';
import {
  ConnectButton,
  ConversationPanel,
  EventsPanel,
  Input,
  UserAudioControl,
} from '@pipecat-ai/voice-ui-kit';

import {
  DEFAULT_LLM,
  DEFAULT_VOICE,
  INITIAL_PUBLIC_KEY,
  LLM_LABELS,
  NEEDS_PUBLIC_KEY,
  setLlm,
  setPublicKey,
  setVoice,
  VOICE_LABELS,
} from '../config';
import type { LlmChoice, TransportType, VoiceChoice } from '../config';
import { OptionSelect } from './OptionSelect';
import { TransportSelect } from './TransportSelect';

interface AppProps extends PipecatBaseChildProps {
  transportType: TransportType;
  onTransportChange: (type: TransportType) => void;
  availableTransports: TransportType[];
}

export const App = ({
  client,
  handleConnect,
  handleDisconnect,
  transportType,
  onTransportChange,
  availableTransports,
}: AppProps) => {
  useEffect(() => {
    client?.initDevices();
  }, [client]);

  const [publicKey, setKey] = useState(INITIAL_PUBLIC_KEY);
  const [llm, setLlmChoice] = useState<LlmChoice>(DEFAULT_LLM);
  const [voice, setVoiceChoice] = useState<VoiceChoice>(DEFAULT_VOICE);

  const showTransportSelector = availableTransports.length > 1;

  return (
    <div className="flex flex-col w-full h-full">
      <div className="flex items-center justify-between gap-4 p-4">
        {showTransportSelector ? (
          <TransportSelect
            transportType={transportType}
            onTransportChange={onTransportChange}
            availableTransports={availableTransports}
          />
        ) : (
          <div /> /* Spacer */
        )}
        <div className="flex items-center gap-4">
          {NEEDS_PUBLIC_KEY && (
            <Input
              type="password"
              autoComplete="off"
              spellCheck={false}
              aria-label="Pipecat Cloud public API key"
              placeholder="Pipecat Cloud key (pk_...)"
              className="w-56"
              value={publicKey}
              onChange={(event) => {
                setKey(event.target.value);
                setPublicKey(event.target.value);
              }}
            />
          )}
          <OptionSelect
            guide="LLM"
            labels={LLM_LABELS}
            value={llm}
            onChange={(choice) => {
              setLlmChoice(choice);
              setLlm(choice);
            }}
          />
          <OptionSelect
            guide="Voice"
            labels={VOICE_LABELS}
            value={voice}
            onChange={(choice) => {
              setVoiceChoice(choice);
              setVoice(choice);
            }}
          />
          <UserAudioControl size="lg" />
          <ConnectButton
            size="lg"
            onConnect={handleConnect}
            onDisconnect={handleDisconnect}
          />
        </div>
      </div>
      <div className="flex-1 overflow-hidden px-4">
        <div className="h-full overflow-hidden">
          <ConversationPanel />
        </div>
      </div>
      <div className="h-96 overflow-hidden px-4 pb-4">
        <EventsPanel />
      </div>
    </div>
  );
};
