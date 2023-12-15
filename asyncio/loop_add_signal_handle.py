"""具体可参照uvicorn中的run方法"""

def install_signal_handlers(self) -> None:
      if threading.current_thread() is not threading.main_thread():
          # Signals can only be listened to from the main thread.
          return

      loop = asyncio.get_event_loop()

      try:
          for sig in HANDLED_SIGNALS:
              loop.add_signal_handler(sig, self.handle_exit, sig, None)
      except NotImplementedError:  # pragma: no cover
          # Windows
          for sig in HANDLED_SIGNALS:
              signal.signal(sig, self.handle_exit)

  def handle_exit(self, sig: signal.Signals, frame: FrameType) -> None:

      if self.should_exit and sig == signal.SIGINT:
          self.force_exit = True
      else:
          self.should_exit = True
