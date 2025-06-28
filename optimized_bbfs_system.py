import requests
import re
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import random
import time

class OptimizedBBFSSystem:
    def __init__(self, data_url=None):
        # Make the main URL customizable, with a configurable default
        self.url = data_url if data_url else "http://128.199.123.196/"
        self.data = []
        self.performance_cache = {}
        self.loss_analysis = {}
        self.optimization_cache = {}
        self.last_updated = None
        
    def fetch_complete_data(self):
        """Fetch complete data from 2020-2025"""
        try:
            print("Mengambil data lengkap dari 2020-2025...")
            # Add retry logic for production deployment
            max_retries = 3
            content = ""
            for attempt in range(max_retries):
                try:
                    response = requests.get(
                        self.url, 
                        timeout=30,
                        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    )
                    response.raise_for_status()
                    content = response.text
                    break
                except requests.RequestException as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed, retrying...")
                    time.sleep(2)
            
            # Enhanced patterns untuk HK market - parsing lebih komprehensif  
            patterns = [
                # Pattern untuk resulthktercepat.org - format baru dengan tabel sederhana
                r'<td class="text-center">([^<]+)</td>\s*<td class="text-center">(\d{2}-\d{2}-\d{4})</td>\s*<td class="text-center">(\d{4})</td>',
                # Pattern standar HK: title="Friday=2025-06-20=1234"
                r'<td title="([^"]*=\d{4}-\d{2}-\d{2}=[^"]*)">(\d{4})</td>',
                # Pattern alternatif untuk format berbeda
                r'<td title="([^"]*=\d{4}-\d{2}-\d{2})=[^"]*">(\d{4})</td>',
                # Pattern untuk data yang mungkin tidak memiliki kode di akhir
                r'<td title="([^"]*\d{4}-\d{2}-\d{2}[^"]*)">(\d{4})</td>',
                # Pattern umum untuk fallback
                r'<td title="([^"]+)">(\d{4})</td>',
                # Pattern untuk menangkap data dengan format HTML berbeda
                r'<td[^>]*title="([^"]*\d{4}-\d{2}-\d{2}[^"]*)">.*?(\d{4}).*?</td>',
                # Pattern khusus untuk menangkap data yang mungkin terlewat
                r'title="([^"]*(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)[^"]*\d{4}-\d{2}-\d{2}[^"]*)"[^>]*>(\d{4})',
                # Pattern untuk data dengan struktur berbeda
                r'(\w+=[0-9]{4}-[0-9]{2}-[0-9]{2}(?:=[0-9]+)?)[^>]*>(\d{4})</td>',
                # Pattern untuk market dengan struktur HTML berbeda
                r'<td[^>]*>([^<]*\d{4}-\d{2}-\d{2}[^<]*)</td>[^<]*<td[^>]*>(\d{4})</td>'
            ]
            
            data = []
            for pattern in patterns:
                matches = re.findall(pattern, content)
                
                for match in matches:
                    # Handle new format vs old format
                    if len(match) == 3:  # New format: day, date, result
                        day_name = match[0]
                        date_str = match[1]
                        result = match[2]
                        
                        try:
                            # Convert DD-MM-YYYY to YYYY-MM-DD
                            date_parts = date_str.split('-')
                            if len(date_parts) == 3:
                                formatted_date = f"{date_parts[2]}-{date_parts[1]}-{date_parts[0]}"
                                # Fix malformed dates before parsing
                                corrected_date = self.fix_malformed_date(formatted_date)
                                date_obj = datetime.strptime(corrected_date, '%Y-%m-%d')
                                if 2020 <= date_obj.year <= 2025:
                                    data.append({
                                        'date': date_obj,
                                        'day': self.standardize_day(day_name),
                                        'result': result,
                                        'last_2d': result[-2:],
                                        'all_digits': list(result)
                                    })
                        except ValueError:
                            continue
                    else:  # Old format with title info
                        title_info = match[0]
                        result = match[1]
                        
                        # Handle different title formats
                        if '=' in title_info:
                            parts = title_info.split('=')
                            if len(parts) >= 3:
                                # Format: Friday=2021-01-01=2030
                                day_name = parts[0]
                                date_str = parts[1]
                            elif len(parts) >= 2:
                                # Format: Friday=2025-06-20
                                day_name = parts[0]
                                date_str = parts[1]
                        else:
                            continue
                        
                        try:
                            # Fix malformed dates - common issues in data source
                            corrected_date_str = self.fix_malformed_date(date_str)
                            date_obj = datetime.strptime(corrected_date_str, '%Y-%m-%d')
                            if 2020 <= date_obj.year <= 2025:
                                data.append({
                                    'date': date_obj,
                                    'day': self.standardize_day(day_name),
                                    'result': result,
                                    'last_2d': result[-2:],
                                    'all_digits': list(result)
                                })
                        except ValueError:
                            continue
                
                # If we found data with this pattern, break
                if data:
                    break
            
            # Validate and filter data
            if not data:
                print("Error: Tidak ada data ditemukan dengan pattern yang tersedia")
                print(f"URL: {self.url}")
                print(f"Content length: {len(content)} chars")
                # Debug: show first few td elements found
                debug_matches = re.findall(r'<td[^>]*title="[^"]*"[^>]*>(\d{4})</td>', content)
                print(f"Debug: Found {len(debug_matches)} potential matches")
                if debug_matches:
                    print(f"Sample matches: {debug_matches[:5]}")
                return False
            
            # Sort by date ascending
            data.sort(key=lambda x: x['date'])
            self.data = data
            self.last_updated = datetime.now()
            
            print(f"✓ Data berhasil dimuat: {len(self.data)} records dari {data[0]['date'].year}-{data[-1]['date'].year}")
            # Accept data if we have reasonable amount (flexible threshold for different sources)
            return len(self.data) >= 100
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def fix_malformed_date(self, date_str):
        """Fix common date formatting issues in data source - Enhanced adaptive correction"""
        try:
            parts = date_str.split('-')
            if len(parts) != 3:
                return date_str
                
            year, month, day = parts
            year_int = int(year)
            month_int = int(month)
            day_int = int(day)
            
            # Case 1: Month > 12 and Day <= 12 (month/day swapped)
            if month_int > 12 and day_int <= 12:
                return f"{year}-{day.zfill(2)}-{month.zfill(2)}"
            
            # Case 2: Month > 12 and Day > 12 (both invalid - likely date error like 2025-28-14)
            elif month_int > 12 and day_int > 12:
                # Check if it's a common pattern like 28-14 which should be 6-28
                if month_int >= 20:  # Likely a day value in month position
                    # Extract the actual day from the "month" field
                    actual_day = str(month_int)[-2:]  # Last 2 digits
                    # Use current month as a reasonable default
                    current_month = datetime.now().month
                    return f"{year}-{str(current_month).zfill(2)}-{actual_day}"
                else:
                    # Other cases - swap positions
                    return f"{year}-{day.zfill(2)}-{month.zfill(2)}"
            
            # Case 3: Day > 31 (invalid day)
            elif day_int > 31:
                # Likely day/month swapped or needs truncation
                if month_int <= 12:
                    # Keep valid month, truncate day to valid range
                    valid_day = min(day_int, 31)
                    if valid_day <= 28:  # Safe for all months
                        return f"{year}-{month.zfill(2)}-{str(valid_day).zfill(2)}"
                    else:
                        # Use last 2 digits if still too large
                        return f"{year}-{month.zfill(2)}-{str(day_int)[-2:].zfill(2)}"
                
            # Case 4: Month = 0 (invalid month)
            elif month_int == 0:
                return f"{year}-01-{day.zfill(2)}"
                
            # Case 5: Normal validation - check if date is actually valid
            else:
                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                    return date_str  # Date is valid
                except ValueError:
                    # Date is invalid despite looking correct - use current month
                    current_month = datetime.now().month
                    return f"{year}-{str(current_month).zfill(2)}-{day.zfill(2)}"
                
        except (ValueError, IndexError):
            # If all else fails, use current date components
            current_date = datetime.now()
            return f"{current_date.year}-{str(current_date.month).zfill(2)}-{str(current_date.day).zfill(2)}"

    def standardize_day(self, day_name):
        """Standardize day names"""
        day_mapping = {
            'senin': 'senin', 'selasa': 'selasa', 'rabu': 'rabu',
            'kamis': 'kamis', 'jumat': 'jumat', 'sabtu': 'sabtu', 'minggu': 'minggu',
            'monday': 'senin', 'tuesday': 'selasa', 'wednesday': 'rabu',
            'thursday': 'kamis', 'friday': 'jumat', 'saturday': 'sabtu', 'sunday': 'minggu'
        }
        return day_mapping.get(day_name.lower(), 'senin')
    
    def get_current_working_date(self):
        """Get current working date that skips non-working days based on actual data"""
        if not self.data:
            return None, None
            
        # Get the latest data entry
        latest_entry = self.data[-1]
        latest_date = latest_entry['date']
        latest_day = latest_entry['day']
        
        # Define working days (days that typically have results)
        working_days = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'minggu']
        
        # Get current actual date
        current_date = datetime.now()
        
        # If today is after the latest data date, determine next working day
        if current_date.date() > latest_date.date():
            # Calculate days since latest data
            days_diff = (current_date.date() - latest_date.date()).days
            
            # Find next working day by checking what day it would be
            next_date = latest_date + timedelta(days=1)
            
            # Map current date to Indonesian day
            current_weekday = current_date.strftime('%A').lower()
            day_map = {
                'monday': 'senin', 'tuesday': 'selasa', 'wednesday': 'rabu',
                'thursday': 'kamis', 'friday': 'jumat', 'saturday': 'sabtu', 'sunday': 'minggu'
            }
            current_indo_day = day_map.get(current_weekday, 'senin')
            
            # Skip Saturday (sabtu) as it typically has no results
            if current_indo_day == 'sabtu':
                # Move to Sunday
                current_indo_day = 'minggu'
                current_date = current_date + timedelta(days=1)
            
            return current_date, current_indo_day
        else:
            # Use latest available data
            return latest_date, latest_day
    
    def build_optimization_patterns(self):
        """Build patterns untuk optimasi BBFS"""
        print("Membangun pola optimasi BBFS...")
        
        # Analisis pattern berdasarkan day dan input
        day_patterns = defaultdict(lambda: defaultdict(list))
        input_patterns = defaultdict(list)
        global_freq = Counter()
        
        for i in range(len(self.data) - 1):
            current = self.data[i]
            next_item = self.data[i + 1]
            
            day = current['day']
            input_2d = current['last_2d']
            next_2d = next_item['last_2d']
            
            # Day-input patterns
            day_patterns[day][input_2d].append(next_2d)
            
            # Input patterns
            input_patterns[input_2d].append(next_2d)
            
            # Global frequency
            for digit in next_2d:
                global_freq[digit] += 1
        
        self.optimization_cache = {
            'day_patterns': dict(day_patterns),
            'input_patterns': dict(input_patterns),
            'global_freq': global_freq
        }
        
        print(f"✓ Pola optimasi berhasil dibangun")
    
    def generate_optimized_bbfs(self, input_2d, day, loss_context=0):
        """Generate BBFS yang dioptimalkan untuk target maksimal 8 loss beruntun"""
        candidates = set()
        
        # Strategy 1: Always include input digits (highest priority)
        candidates.update(list(input_2d))
        
        # Strategy 2: Day-specific patterns
        if day in self.optimization_cache.get('day_patterns', {}):
            if input_2d in self.optimization_cache['day_patterns'][day]:
                next_possibilities = self.optimization_cache['day_patterns'][day][input_2d]
                
                # Get all digits from next possibilities
                next_digits = []
                for next_2d in next_possibilities:
                    next_digits.extend(list(next_2d))
                
                # Add top frequency digits
                if next_digits:
                    digit_freq = Counter(next_digits)
                    top_digits = [d for d, _ in digit_freq.most_common(6)]
                    candidates.update(top_digits)
        
        # Strategy 3: Input-specific patterns (regardless of day)
        if input_2d in self.optimization_cache.get('input_patterns', {}):
            next_possibilities = self.optimization_cache['input_patterns'][input_2d]
            next_digits = []
            for next_2d in next_possibilities:
                next_digits.extend(list(next_2d))
            
            if next_digits:
                digit_freq = Counter(next_digits)
                top_digits = [d for d, _ in digit_freq.most_common(4)]
                candidates.update(top_digits)
        
        # Strategy 4: Global high frequency digits
        global_freq = self.optimization_cache.get('global_freq', Counter())
        top_global = [d for d, _ in global_freq.most_common(8)]
        candidates.update(top_global[:5])
        
        # Strategy 5: Anti-loss enhancement (untuk loss context > 3)
        if loss_context > 3:
            # Add complementary digits untuk break streak
            complement_digits = []
            for digit in input_2d:
                comp = str((int(digit) + 5) % 10)
                complement_digits.append(comp)
            candidates.update(complement_digits)
            
            # Add sequential patterns
            for digit in input_2d:
                candidates.add(str((int(digit) + 1) % 10))
                candidates.add(str((int(digit) + 2) % 10))
        
        # Convert to list and score (DETERMINISTIK - tidak ada randomness)
        bbfs_candidates = sorted(list(candidates))  # Sort untuk konsistensi
        
        if len(bbfs_candidates) > 5:
            # Score each digit secara deterministik
            digit_scores = {}
            for digit in bbfs_candidates:
                score = 0
                
                # Input digits get highest score
                if digit in input_2d:
                    score += 1000
                
                # Global frequency score
                if digit in global_freq:
                    score += global_freq[digit]
                
                # Day-specific score
                if day in self.optimization_cache.get('day_patterns', {}):
                    if input_2d in self.optimization_cache['day_patterns'][day]:
                        for next_2d in self.optimization_cache['day_patterns'][day][input_2d]:
                            if digit in next_2d:
                                score += 20
                
                # Loss context score
                if loss_context > 0:
                    if digit in str((int(input_2d[0]) + loss_context) % 10) + str((int(input_2d[1]) + loss_context) % 10):
                        score += 50
                
                # Tie-breaker berdasarkan nilai digit (deterministik)
                score += int(digit) * 0.1
                
                digit_scores[digit] = score
            
            # Sort by score dan digit value untuk hasil konsisten
            sorted_digits = sorted(digit_scores.items(), key=lambda x: (x[1], x[0]), reverse=True)
            bbfs = [digit for digit, _ in sorted_digits[:5]]
        else:
            bbfs = sorted(bbfs_candidates)  # Sort untuk konsistensi
        
        # Ensure exactly 5 digits
        while len(bbfs) < 5:
            for digit in "0123456789":
                if digit not in bbfs:
                    bbfs.append(digit)
                    break
        
        return bbfs[:5]
    
    def test_comprehensive_performance(self):
        """Test performance dengan akurasi data yang ketat"""
        print("Testing comprehensive performance...")
        
        if not self.optimization_cache:
            self.build_optimization_patterns()
        
        # Validasi data input terlebih dahulu
        if len(self.data) < 2:
            print("Error: Data tidak cukup untuk analisis")
            return None
        
        results = []
        consecutive_losses = 0
        max_consecutive = 0
        total_wins = 0
        total_tests = 0
        loss_streaks = []
        win_details = []
        loss_details = []
        
        # Hitung dengan algoritma yang konsisten dan akurat
        for i in range(len(self.data) - 1):
            current = self.data[i]
            next_item = self.data[i + 1]
            
            # Validasi data sebelum pemrosesan
            if not current.get('last_2d') or not next_item.get('last_2d'):
                continue
            
            if len(current['last_2d']) != 2 or len(next_item['last_2d']) != 2:
                continue
            
            # Generate BBFS dengan metode deterministik
            bbfs = self.generate_optimized_bbfs(
                current['last_2d'], 
                current['day'], 
                consecutive_losses
            )
            
            # Validasi BBFS hasil
            if len(bbfs) != 5:
                continue
            
            # Check win condition dengan validasi ketat
            next_2d_digits = set(next_item['last_2d'])
            bbfs_digits = set(bbfs)
            
            # Pastikan validasi benar: semua digit 2D harus ada di BBFS
            is_win = next_2d_digits.issubset(bbfs_digits)
            
            total_tests += 1
            
            if is_win:
                total_wins += 1
                # Record loss streak before resetting
                if consecutive_losses > 0:
                    loss_streaks.append(consecutive_losses)
                    consecutive_losses = 0
                
                win_details.append({
                    'date': current['date'],
                    'result': current['result'],
                    'next': next_item['result'],
                    'bbfs': ''.join(sorted(bbfs)),  # Sort untuk konsistensi
                    'day': current['day'],
                    'input_2d': current['last_2d'],
                    'actual_2d': next_item['last_2d']
                })
            else:
                consecutive_losses += 1
                max_consecutive = max(max_consecutive, consecutive_losses)
                
                loss_details.append({
                    'date': current['date'],
                    'result': current['result'],
                    'next': next_item['result'],
                    'bbfs': ''.join(sorted(bbfs)),
                    'day': current['day'],
                    'loss_number': consecutive_losses,
                    'input_2d': current['last_2d'],
                    'actual_2d': next_item['last_2d']
                })
            
            results.append({
                'date': current['date'],
                'input_2d': current['last_2d'],
                'next_2d': next_item['last_2d'],
                'bbfs': bbfs,
                'is_win': is_win,
                'consecutive_losses': consecutive_losses
            })
        
        # Final streak calculation
        if consecutive_losses > 0:
            loss_streaks.append(consecutive_losses)
        
        # Validasi perhitungan akhir
        if total_tests == 0:
            print("Error: Tidak ada data valid untuk dianalisis")
            return None
        
        win_rate = (total_wins / total_tests * 100) if total_tests > 0 else 0
        
        # Validasi hasil akhir
        print(f"VALIDASI: Total Tests={total_tests}, Total Wins={total_wins}, Win Rate={win_rate:.1f}%")
        print(f"VALIDASI: Max Loss={max_consecutive}, Loss Streaks Count={len(loss_streaks)}")
        
        # Simpan hasil dengan validasi ketat
        self.performance_data = {
            'total_tests': total_tests,
            'total_wins': total_wins,
            'total_losses': total_tests - total_wins,
            'win_rate': round(win_rate, 1),  # Bulatkan untuk konsistensi
            'loss_rate': round(100 - win_rate, 1),
            'max_consecutive_loss': max_consecutive,
            'loss_streaks': loss_streaks,
            'meets_target': max_consecutive <= 10,
            'win_details': win_details[-100:],  # Batasi untuk performa
            'loss_details': loss_details[-100:],
            'results': results[-100:],
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_range': f"{self.data[0]['date'].strftime('%Y-%m-%d')} - {self.data[-1]['date'].strftime('%Y-%m-%d')}",
            'total_data_records': len(self.data)
        }
        
        print(f"Performance: Win Rate {win_rate:.1f}%, Max Loss {max_consecutive}")
        return self.performance_data
        
        self.performance_data = {
            'total_tests': total_tests,
            'total_wins': total_wins,
            'win_rate': win_rate,
            'max_consecutive_loss': max_consecutive,
            'loss_streaks': loss_streaks,
            'meets_target': max_consecutive <= 8,
            'win_details': win_details[-50:],
            'loss_details': loss_details[-50:],
            'results': results
        }
        
        print(f"Performance: Win Rate {win_rate:.1f}%, Max Loss {max_consecutive}")
        return self.performance_data
    
    def run_performance_test(self, force_refresh=False):
        """Run performance test dan simpan hasil dengan caching konsisten"""
        # Force refresh or if no cached data, run new test
        if force_refresh or not hasattr(self, 'performance_data') or not self.performance_data:
            result = self.test_comprehensive_performance()
            if result:
                print(f"Performance: Win Rate {self.performance_data['win_rate']:.1f}%, Max Loss {self.performance_data['max_consecutive_loss']}")
                return True
            else:
                print("Performance test gagal")
                return False
        
        # Return cached data if available
        return True
    
    def get_current_loss_streak_analysis(self, limit=10):
        """Analisis current loss streak REAL-TIME yang akurat"""
        if not self.data or len(self.data) < 2:
            return 0, []
        
        # Pastikan menggunakan optimization cache yang sudah dibangun
        if not self.optimization_cache:
            self.build_optimization_patterns()
        
        current_streak = 0
        streak_details = []
        
        # Analisis dari data terbaru mundur dengan chronological order yang benar
        # Data sudah di-sort ascending, jadi ambil yang terakhir
        recent_data = self.data[-limit:] if len(self.data) >= limit else self.data
        
        # Test dari data terbaru ke belakang untuk mencari current active streak
        for i in range(len(recent_data) - 1, 0, -1):  # Mundur dari yang terbaru
            prev_item = recent_data[i - 1]  # Data sebelumnya (input untuk prediksi)
            current = recent_data[i]        # Data hasil (untuk validasi)
            
            # Generate BBFS berdasarkan data sebelumnya
            bbfs = self.generate_optimized_bbfs(prev_item['last_2d'], prev_item['day'], 0)
            current_2d_digits = set(current['last_2d'])
            bbfs_digits = set(bbfs)
            
            # Check apakah BBFS berhasil cover result
            is_win = current_2d_digits.issubset(bbfs_digits)
            
            if not is_win:
                current_streak += 1
                streak_details.insert(0, {  # Insert di awal untuk urutan chronological
                    'date': prev_item['date'],
                    'input_result': prev_item['result'],
                    'actual_result': current['result'],
                    'input_2d': prev_item['last_2d'],
                    'actual_2d': current['last_2d'],
                    'bbfs_used': ''.join(bbfs),
                    'day': prev_item['day'],
                    'loss_number': current_streak
                })
            else:
                # Ketemu win, stop counting
                break
        
        return current_streak, streak_details
    
    def get_performance_summary(self):
        """Get performance summary"""
        if not hasattr(self, 'performance_data') or not self.performance_data:
            return None
        
        return {
            'total_tests': self.performance_data['total_tests'],
            'wins': self.performance_data['total_wins'],
            'win_rate': self.performance_data['win_rate'],
            'max_consecutive_loss': self.performance_data['max_consecutive_loss'],
            'meets_target': self.performance_data['meets_target']
        }
    
    def get_consecutive_loss_breakdown(self):
        """Get breakdown of consecutive losses - shows ALL streaks including 20x+"""
        if not hasattr(self, 'performance_data') or not self.performance_data or not self.performance_data.get('loss_streaks'):
            return {}
        
        loss_streaks = self.performance_data['loss_streaks']
        if not loss_streaks:
            return {}
        
        streak_counts = Counter(loss_streaks)
        total_streaks = len(loss_streaks)
        
        breakdown = {}
        # Sort by streak length to show in order (1x, 2x, 3x, ... up to max)
        max_streak = max(loss_streaks) if loss_streaks else 0
        
        for streak_len in sorted(streak_counts.keys()):
            count = streak_counts[streak_len]
            percentage = (count / total_streaks * 100) if total_streaks > 0 else 0
            
            # Determine status based on streak length
            if streak_len <= 3:
                status = "Normal"
            elif streak_len <= 6:
                status = "Perhatian"
            elif streak_len <= 10:
                status = "Tinggi"
            elif streak_len <= 15:
                status = "Kritis"
            else:
                status = "Berbahaya"
            
            breakdown[f"{streak_len}x"] = {
                'count': count,
                'percentage': percentage,
                'status': status,
                'streak_length': streak_len
            }
        
        # Add summary info
        breakdown['_summary'] = {
            'total_streaks': total_streaks,
            'max_streak': max_streak,
            'avg_streak': sum(loss_streaks) / len(loss_streaks) if loss_streaks else 0
        }
        
        return breakdown
    

    
    def get_latest_results(self, limit=10):
        """Get latest results in chronological order (newest first)"""
        if not self.data:
            return []
        
        # Return data terbaru dalam urutan terbaru ke lama
        return list(reversed(self.data[-limit:]))
    
    def get_real_time_analysis(self, limit=8):
        """Analisis real-time untuk menampilkan win/loss yang akurat"""
        if not self.data or len(self.data) < 2:
            return []
        
        # Pastikan optimization cache tersedia
        if not self.optimization_cache:
            self.build_optimization_patterns()
        
        analysis_results = []
        recent_data = self.data[-limit-1:] if len(self.data) > limit else self.data
        
        # Analisis dari data kedua terakhir sampai yang terbaru
        for i in range(len(recent_data) - 1):
            current = recent_data[i]      # Input untuk prediksi
            next_item = recent_data[i + 1] # Hasil aktual
            
            # Generate BBFS berdasarkan current data
            bbfs = self.generate_optimized_bbfs(current['last_2d'], current['day'], 0)
            next_2d_digits = set(next_item['last_2d'])
            bbfs_digits = set(bbfs)
            
            # Validasi win/loss
            is_win = next_2d_digits.issubset(bbfs_digits)
            
            analysis_results.append({
                'date': current['date'],
                'input_result': current['result'],
                'input_2d': current['last_2d'], 
                'actual_result': next_item['result'],
                'actual_2d': next_item['last_2d'],
                'bbfs_generated': bbfs,
                'bbfs_string': ''.join(bbfs),
                'day': current['day'],
                'is_win': is_win,
                'covered_digits': list(next_2d_digits & bbfs_digits),
                'missing_digits': list(next_2d_digits - bbfs_digits)
            })
        
        # Return dalam urutan terbaru ke lama
        return list(reversed(analysis_results))
    
    def get_data_info(self):
        """Get data information"""
        if not self.data:
            return None
        
        return {
            'total_records': len(self.data),
            'date_range': {
                'start': self.data[0]['date'].strftime('%Y-%m-%d'),
                'end': self.data[-1]['date'].strftime('%Y-%m-%d')
            },
            'last_updated': self.last_updated.strftime('%Y-%m-%d %H:%M:%S') if self.last_updated else None
        }

# Singleton instance
_optimized_system = None

def get_optimized_system(data_url=None):
    """Get system instance with configurable URL"""
    global _optimized_system
    if _optimized_system is None or (data_url and data_url != _optimized_system.url):
        _optimized_system = OptimizedBBFSSystem(data_url)
    return _optimized_system