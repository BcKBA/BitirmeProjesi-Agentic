"use client";

import { cn } from "@/lib/utils";
import { BrainCircuit, Layers } from "lucide-react";

export const AGENTS = [
  {
    id: "agent",
    label: "Deep Agent",
    description: "Hierarchical architecture with planning, sub-agents & filesystem",
    icon: Layers,
  },
  {
    id: "baseline_agent",
    label: "Baseline Agent",
    description: "Standard ReAct-style agent with read_file, get_repo_structure & search_rag",
    icon: BrainCircuit,
  },
] as const;

export type AgentId = (typeof AGENTS)[number]["id"];

interface AgentSelectorProps {
  value: AgentId;
  onChange: (id: AgentId) => void;
  disabled?: boolean;
}

export function AgentSelector({ value, onChange, disabled }: AgentSelectorProps) {
  return (
    <div className="flex flex-col gap-2 w-full max-w-xl">
      <span className="text-sm font-medium text-gray-500">Select Agent</span>
      <div className="grid grid-cols-2 gap-2">
        {AGENTS.map(({ id, label, description, icon: Icon }) => (
          <button
            key={id}
            type="button"
            disabled={disabled}
            onClick={() => onChange(id)}
            className={cn(
              "flex flex-col items-start gap-1 rounded-xl border p-3 text-left transition-all",
              value === id
                ? "border-blue-500 bg-blue-50 shadow-sm"
                : "border-gray-200 bg-white hover:border-gray-300 hover:bg-gray-50",
              disabled && "cursor-not-allowed opacity-50",
            )}
          >
            <div className="flex items-center gap-2">
              <Icon
                className={cn(
                  "size-4",
                  value === id ? "text-blue-600" : "text-gray-500",
                )}
              />
              <span
                className={cn(
                  "text-sm font-semibold",
                  value === id ? "text-blue-700" : "text-gray-700",
                )}
              >
                {label}
              </span>
            </div>
            <p className="text-xs text-gray-500 leading-snug">{description}</p>
          </button>
        ))}
      </div>
    </div>
  );
}

interface AgentBadgeProps {
  agentId: string;
}

export function AgentBadge({ agentId }: AgentBadgeProps) {
  const agent = AGENTS.find((a) => a.id === agentId);
  if (!agent) return null;
  const Icon = agent.icon;
  return (
    <div className="flex items-center gap-1.5 rounded-full border border-blue-200 bg-blue-50 px-2.5 py-1 text-xs font-medium text-blue-700">
      <Icon className="size-3.5" />
      {agent.label}
    </div>
  );
}
