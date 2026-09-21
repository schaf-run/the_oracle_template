import { useState } from "react";

interface ShareLinkProps {
  id: string;
}

export function ShareLink({ id }: ShareLinkProps) {
  const [copied, setCopied] = useState(false);
  const url = `${window.location.origin}/model/${id}`;

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // clipboard API unavailable — user can still select/copy the text manually
    }
  };

  return (
    <div>
      <a href={`/model/${id}`}>{url}</a>
      <button type="button" onClick={copy}>
        {copied ? "Copied!" : "Copy link"}
      </button>
    </div>
  );
}
