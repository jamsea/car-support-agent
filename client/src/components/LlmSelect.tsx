import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
  SelectGuide,
} from '@pipecat-ai/voice-ui-kit';

import { LLM_LABELS, type LlmChoice } from '../config';

interface LlmSelectProps {
  llm: LlmChoice;
  onLlmChange: (llm: LlmChoice) => void;
}

export const LlmSelect = ({ llm, onLlmChange }: LlmSelectProps) => {
  return (
    <Select value={llm} onValueChange={onLlmChange}>
      <SelectTrigger size="lg">
        <SelectGuide>LLM</SelectGuide>
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        {(Object.keys(LLM_LABELS) as LlmChoice[]).map((choice) => (
          <SelectItem key={choice} value={choice}>
            {LLM_LABELS[choice]}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
};
