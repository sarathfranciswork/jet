export interface ICycleGroupIcon {
  className?: string;
  color?: string;
  cycleGroup: TCycleGroups;
  height?: string;
  width?: string;
}

export type TCycleGroups = "current" | "upcoming" | "completed" | "draft";

export const CYCLE_GROUP_COLORS: {
  [key in TCycleGroups]: string;
} = {
  current: "#F59E0B",
  upcoming: "#3B82F6",
  completed: "#16A34A",
  draft: "#525252",
};
