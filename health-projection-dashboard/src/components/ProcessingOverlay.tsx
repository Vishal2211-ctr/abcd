const ProcessingOverlay = () => {
  return (
    <>
      <div className="processing-bg" />
      <div className="processing-overlay">
        <p className="font-mono-data text-muted-foreground text-lg font-light tracking-wide">
          Processing Handwriting with NLPformed
          <span className="inline-block w-2 h-2 rounded-full bg-primary ml-1 animate-pulse-dot" />
        </p>
      </div>
    </>
  );
};

export default ProcessingOverlay;
