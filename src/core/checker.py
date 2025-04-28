"""
生日检查模块
"""
from datetime import datetime, timedelta, date
from typing import List, Tuple, Dict, Union
from lunar_python import Solar
from src.core.config import Recipient
import logging

logger = logging.getLogger(__name__)


class BirthdayChecker:
    def check_birthdays(self, recipients: List[Recipient]) -> List[Tuple[Recipient, bool, Dict]]:
        """
        检查所有人的生日

        Args:
            recipients: 收件人列表

        Returns:
            List[Tuple[Recipient, bool, Dict]]: 返回收件人、是否生日和额外信息的元组列表
        """
        today = datetime.now()
        results = []

        for recipient in recipients:
            is_birthday, extra_info = self._check_birthday(recipient, today)
            results.append((recipient, is_birthday, extra_info))

        return results

    def _convert_to_date_parts(self, date_obj: Union[str, datetime, date]) -> Tuple[int, int, int]:
        """
        转换日期为年月日元组

        Args:
            date_obj: 日期对象，可以是字符串、datetime或date类型

        Returns:
            Tuple[int, int, int]: 年月日的元组
        """
        if isinstance(date_obj, str):
            dt = datetime.strptime(date_obj, "%Y-%m-%d")
        elif isinstance(date_obj, datetime):
            dt = date_obj
        elif isinstance(date_obj, date):
            dt = datetime.combine(date_obj, datetime.min.time())
        else:
            raise ValueError(f"Unsupported date type: {type(date_obj)}")
        return dt.year, dt.month, dt.day

    def _check_birthday(self, recipient: Recipient, today: datetime) -> Tuple[bool, Dict]:
        """
        检查是否是生日（包括提前提醒）

        Args:
            recipient: 收件人信息
            today: 当前日期

        Returns:
            Tuple[bool, Dict]: 是否是生日和额外信息
        """
        try:
            check_dates = []
            for i in range(recipient.reminder_days + 1):
                check_date = today + timedelta(days=i)
                check_dates.append(check_date)

            extra_info = {
                'solar_match': False,
                'lunar_match': False,
                'days_until': 0,
                'zodiac': '',           # 生肖
                'gz_year': '',          # 干支纪年
                'gz_month': '',         # 干支纪月
                'gz_day': '',           # 干支纪日
                'gz_hour': '',          # 干支纪时
                'lunar_month': '',      # 农历月份
                'lunar_day': '',        # 农历日期
                'lunar_festival': '',   # 农历节日
                'solar_festival': '',   # 阳历节日
                'solar_term': '',       # 节气
                'age': 0,
                'week_name': '',        # 星期
                'constellation': ''     # 星座
            }

            # 获取今天的详细信息
            year, month, day = self._convert_to_date_parts(today)
            today_solar = Solar.fromYmd(year, month, day)
            today_lunar = today_solar.getLunar()

            # 填充当天信息
            extra_info.update({
                'gz_year': today_lunar.getYearInGanZhi(),
                'gz_month': today_lunar.getMonthInGanZhi(),
                'gz_day': today_lunar.getDayInGanZhi(),
                'gz_hour': today_lunar.getTimeInGanZhi(),
                'lunar_month': f"{today_lunar.getMonthInChinese()}月",
                'lunar_day': today_lunar.getDayInChinese(),
                'week_name': today_solar.getWeekInChinese(),
                'constellation': today_solar.getXingZuo(),
            })

            # 获取节日信息
            lunar_festivals = today_lunar.getFestivals()
            if lunar_festivals:
                extra_info['lunar_festival'] = '、'.join(lunar_festivals)

            solar_festivals = today_solar.getFestivals()
            if solar_festivals:
                extra_info['solar_festival'] = '、'.join(solar_festivals)

            # 获取节气
            term = today_lunar.getJieQi()
            if term:
                extra_info['solar_term'] = term

            # 检查阳历生日
            if recipient.solar_birthday:
                try:
                    birth_year, birth_month, birth_day = self._convert_to_date_parts(
                        recipient.solar_birthday)
                    for i, check_date in enumerate(check_dates):
                        year, month, day = self._convert_to_date_parts(check_date)
                        if month == birth_month and day == birth_day:
                            extra_info['solar_match'] = True
                            extra_info['days_until'] = i
                            extra_info['age'] = year - birth_year
                            break
                except ValueError as e:
                    logger.error(f"Invalid solar birthday format for {recipient.name}: {e}")

            # 检查农历生日
            if recipient.lunar_birthday:
                try:
                    birth_year, birth_month, birth_day = self._convert_to_date_parts(
                        recipient.lunar_birthday)
                    for i, check_date in enumerate(check_dates):
                        year, month, day = self._convert_to_date_parts(check_date)
                        check_solar = Solar.fromYmd(year, month, day)
                        check_lunar = check_solar.getLunar()
                        if (check_lunar.getMonth() == birth_month
                                and check_lunar.getDay() == birth_day):
                            extra_info['lunar_match'] = True
                            extra_info['days_until'] = i
                            extra_info['age'] = year - birth_year
                            break
                except ValueError as e:
                    logger.error(f"Invalid lunar birthday format for {recipient.name}: {e}")

            # 如果是生日，添加生肖和其他信息
            if extra_info['solar_match'] or extra_info['lunar_match']:
                try:
                    # 获取生肖和其他信息
                    if recipient.lunar_birthday:
                        year, month, day = self._convert_to_date_parts(
                            recipient.lunar_birthday)
                    else:
                        year, month, day = self._convert_to_date_parts(
                            recipient.solar_birthday)

                    birth_solar = Solar.fromYmd(year, month, day)
                    birth_lunar = birth_solar.getLunar()
                    extra_info['zodiac'] = birth_lunar.getYearShengXiao()
                except Exception as e:
                    logger.error(f"Failed to get zodiac info for {recipient.name}: {e}")

            return (extra_info['solar_match'] or extra_info['lunar_match']), extra_info
        except Exception as e:
            logger.error(f"Error checking birthday for {recipient.name}: {e}")
            return False, {}
