#ifdef USE_BK72XX
#include "deep_sleep_component.h"

#include <libretiny.h>

namespace esphome {
namespace deep_sleep {

static const char *const TAG = "deep_sleep";

void DeepSleepComponent::set_wakeup_pin_mode(WakeupPinMode wakeup_pin_mode) {
  this->wakeup_pin_mode_ = wakeup_pin_mode;
}

optional<uint32_t> DeepSleepComponent::get_run_duration_() const { return this->run_duration_; }

void DeepSleepComponent::dump_config_platform_() {}

bool DeepSleepComponent::prepare_to_sleep_() {
  if (this->wakeup_pin_mode_ == WAKEUP_PIN_MODE_KEEP_AWAKE && this->wakeup_pin_ != nullptr &&
      this->wakeup_pin_->digital_read()) {
    lt_deep_sleep_config_gpio(uint32_t gpio_index_map, true);
  }
  return true;
}

void DeepSleepComponent::deep_sleep_() { lt_deep_sleep_enter(); }

}  // namespace deep_sleep
}  // namespace esphome
#endif
