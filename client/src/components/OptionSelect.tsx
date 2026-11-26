import {
  Select,
  SelectTrigger,
  SelectValue,
  SelectContent,
  SelectItem,
  SelectGuide,
} from '@pipecat-ai/voice-ui-kit';

interface OptionSelectProps<T extends string> {
  guide: string;
  labels: Record<T, string>;
  value: T;
  onChange: (value: T) => void;
}

/** A labelled dropdown for one of the call options (LLM, voice). */
export const OptionSelect = <T extends string>({
  guide,
  labels,
  value,
  onChange,
}: OptionSelectProps<T>) => {
  return (
    <Select value={value} onValueChange={onChange}>
      <SelectTrigger size="lg">
        <SelectGuide>{guide}</SelectGuide>
        <SelectValue />
      </SelectTrigger>
      <SelectContent>
        {(Object.keys(labels) as T[]).map((option) => (
          <SelectItem key={option} value={option}>
            {labels[option]}
          </SelectItem>
        ))}
      </SelectContent>
    </Select>
  );
};
