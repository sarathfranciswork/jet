import { FC } from "react";
import { IGithubPullRequest } from "types";

type Props = {
  pullRequest: IGithubPullRequest;
};

const STATE_STYLES: Record<string, { bg: string; text: string; label: string }> = {
  draft: { bg: "bg-gray-500/20", text: "text-gray-500", label: "Draft" },
  open: { bg: "bg-green-500/20", text: "text-green-500", label: "Open" },
  closed: { bg: "bg-red-500/20", text: "text-red-500", label: "Closed" },
  merged: { bg: "bg-purple-500/20", text: "text-purple-500", label: "Merged" },
};

export const PrBadge: FC<Props> = ({ pullRequest }) => {
  const style = STATE_STYLES[pullRequest.state] || STATE_STYLES.open;

  return (
    <a
      href={pullRequest.url}
      target="_blank"
      rel="noopener noreferrer"
      className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-xs ${style.bg} ${style.text} hover:opacity-80 transition-opacity`}
    >
      <svg
        className="h-3.5 w-3.5"
        viewBox="0 0 16 16"
        fill="currentColor"
      >
        <path d="M7.177 3.073L9.573.677A.25.25 0 0110 .854v4.792a.25.25 0 01-.427.177L7.177 3.427a.25.25 0 010-.354zM3.75 2.5a.75.75 0 100 1.5.75.75 0 000-1.5zm-2.25.75a2.25 2.25 0 113 2.122v5.256a2.251 2.251 0 11-1.5 0V5.372A2.25 2.25 0 011.5 3.25zM11 2.5h-1V4h1a1 1 0 011 1v5.628a2.251 2.251 0 101.5 0V5A2.5 2.5 0 0011 2.5zm1 10.25a.75.75 0 111.5 0 .75.75 0 01-1.5 0zM3.75 12a.75.75 0 100 1.5.75.75 0 000-1.5z" />
      </svg>
      <span>
        #{pullRequest.pr_number} {style.label}
      </span>
      {pullRequest.triggers_automation && (
        <span className="text-[10px] opacity-75">auto</span>
      )}
    </a>
  );
};
