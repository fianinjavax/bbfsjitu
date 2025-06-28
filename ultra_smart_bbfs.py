import requests
import re
from datetime import datetime
import random
import json
from collections import defaultdict, Counter
import itertools
import time
import math

class UltraSmartBBFS:
    def __init__(self, data_url=None):
        # Support for different markets
        self.url = data_url if data_url else "http://128.199.123.196/"
        self.data = []
        self.transition_matrix = {}
        self.day_patterns = {}
        self.digit_frequency = {}
        self.winning_sequences = []
        self.loss_patterns = {}
        self.best_strategy = None
        
    def load_and_process_data(self):
        """Load data dengan preprocessing yang lebih canggih"""
        print("Mengunduh dan memproses data dengan analisis mendalam...")
        
        try:
            response = requests.get(self.url, timeout=30)
            content = response.text
            
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
                r'(\w+=[0-9]{4}-[0-9]{2}-[0-9]{2}(?:=[0-9]+)?)[^>]*>(\d{4})</td>'
            ]
            
            raw_data = []
            for pattern in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    break
            
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
                                day_std = self.standardize_day(day_name)
                                if day_std:
                                    raw_data.append({
                                        'date': date_obj,
                                        'day': day_std,
                                        'result': result,
                                        'last_2d': result[-2:],
                                        'digits': [int(d) for d in result],
                                        'digit_sum': sum(int(d) for d in result),
                                        'digit_product': math.prod(int(d) for d in result if int(d) > 0),
                                        'even_count': sum(1 for d in result if int(d) % 2 == 0),
                                        'odd_count': sum(1 for d in result if int(d) % 2 == 1)
                                    })
                    except ValueError:
                        continue
                else:  # Old format with title info
                    title_info = match[0]
                    result = match[1]
                    
                    parts = title_info.split('=')
                    if len(parts) >= 2:
                        day_name = parts[0].strip()
                        date_str = parts[1].strip()
                    
                    try:
                        # Fix malformed dates before parsing
                        corrected_date_str = self.fix_malformed_date(date_str)
                        date_obj = datetime.strptime(corrected_date_str, '%Y-%m-%d')
                        if 2020 <= date_obj.year <= 2025:
                            day_std = self.standardize_day(day_name)
                            if day_std:
                                raw_data.append({
                                    'date': date_obj,
                                    'day': day_std,
                                    'result': result,
                                    'last_2d': result[-2:],
                                    'digits': [int(d) for d in result],
                                    'digit_sum': sum(int(d) for d in result),
                                    'digit_product': math.prod(int(d) for d in result if int(d) > 0),
                                    'even_count': sum(1 for d in result if int(d) % 2 == 0),
                                    'odd_count': sum(1 for d in result if int(d) % 2 == 1)
                                })
                    except ValueError:
                        continue
            
            # Sort by date
            raw_data.sort(key=lambda x: x['date'])
            self.data = raw_data
            
            print(f"Loaded {len(self.data)} records from 2020-2025")
            return len(self.data) >= 1200
            
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
                # Likely day/month swapped
                if month_int <= 12:
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
        day_map = {
            'senin': 'Senin', 'monday': 'Senin', 'mon': 'Senin',
            'selasa': 'Selasa', 'tuesday': 'Selasa', 'tue': 'Selasa', 
            'rabu': 'Rabu', 'wednesday': 'Rabu', 'wed': 'Rabu',
            'kamis': 'Kamis', 'thursday': 'Kamis', 'thu': 'Kamis',
            'jumat': 'Jumat', 'friday': 'Jumat', 'fri': 'Jumat',
            'sabtu': 'Sabtu', 'saturday': 'Sabtu', 'sat': 'Sabtu',
            'minggu': 'Minggu', 'sunday': 'Minggu', 'sun': 'Minggu'
        }
        return day_map.get(day_name.lower().strip())
    
    def deep_pattern_analysis(self):
        """Analisis pola yang sangat mendalam"""
        print("Melakukan analisis pola ultra-mendalam...")
        
        # Matrix transisi 2D -> 2D
        transitions = defaultdict(list)
        
        # Pattern per hari
        day_transitions = defaultdict(lambda: defaultdict(list))
        
        # Analisis digit frequency setelah input tertentu
        digit_after_input = defaultdict(lambda: defaultdict(int))
        
        # Pattern loss sequences
        loss_sequences = defaultdict(int)
        
        # Pattern winning after loss
        win_after_loss = defaultdict(list)
        
        for i in range(len(self.data) - 1):
            current = self.data[i]
            next_item = self.data[i + 1]
            
            curr_2d = current['last_2d']
            next_2d = next_item['last_2d']
            day = current['day']
            
            # Basic transitions
            transitions[curr_2d].append(next_2d)
            day_transitions[day][curr_2d].append(next_2d)
            
            # Digit frequency analysis
            for digit in next_2d:
                digit_after_input[curr_2d][digit] += 1
        
        # Advanced loss pattern analysis
        self.analyze_loss_patterns()
        
        self.transition_matrix = dict(transitions)
        self.day_patterns = dict(day_transitions)
        self.digit_frequency = dict(digit_after_input)
        
        print(f"Completed deep analysis: {len(self.transition_matrix)} transition patterns")
    
    def analyze_loss_patterns(self):
        """Analisis pola khusus untuk mengurangi consecutive losses"""
        print("Menganalisis pola consecutive losses...")
        
        # Simulasi untuk menemukan pola loss
        temp_results = []
        consecutive_count = 0
        
        for i in range(min(1200, len(self.data) - 1)):
            current = self.data[i]
            next_item = self.data[i + 1]
            
            # Simulasi dengan strategi dasar
            basic_bbfs = self.generate_basic_bbfs(current['last_2d'], current['day'])
            next_2d_set = set(next_item['last_2d'])
            bbfs_set = set(basic_bbfs)
            
            is_win = next_2d_set.issubset(bbfs_set)
            
            if not is_win:
                consecutive_count += 1
            else:
                if consecutive_count > 0:
                    # Record pattern sebelum win
                    pattern_key = f"loss_{consecutive_count}"
                    self.loss_patterns[pattern_key] = self.loss_patterns.get(pattern_key, 0) + 1
                consecutive_count = 0
        
        print(f"Loss pattern analysis complete: {len(self.loss_patterns)} patterns found")
    
    def generate_basic_bbfs(self, input_2d, day):
        """Basic BBFS generation untuk analisis"""
        digits = list(input_2d)
        while len(digits) < 5:
            new_digit = str(random.randint(0, 9))
            if new_digit not in digits:
                digits.append(new_digit)
        return digits[:5]
    
    def generate_smart_bbfs(self, input_2d, day, strategy_type="ultra"):
        """Generate BBFS dengan strategi ultra-cerdas"""
        
        # Analisis konteks
        context_score = self.calculate_context_score(input_2d, day)
        
        # Kandidat digit berdasarkan multiple criteria
        candidates = self.get_smart_candidates(input_2d, day, context_score)
        
        # Apply different strategies based on type
        if strategy_type == "ultra":
            return self.ultra_strategy(input_2d, candidates, context_score)
        elif strategy_type == "defensive":
            return self.defensive_strategy(input_2d, candidates)
        elif strategy_type == "aggressive":
            return self.aggressive_strategy(input_2d, candidates)
        else:
            return self.balanced_strategy(input_2d, candidates)
    
    def calculate_context_score(self, input_2d, day):
        """Hitung skor konteks untuk strategi adaptif"""
        score = 0
        
        # Day weight
        day_weights = {
            'Senin': 1.0, 'Selasa': 1.1, 'Rabu': 0.9, 'Kamis': 1.2,
            'Jumat': 0.8, 'Sabtu': 1.3, 'Minggu': 0.7
        }
        score += day_weights.get(day, 1.0)
        
        # Input digit analysis
        digit1, digit2 = int(input_2d[0]), int(input_2d[1])
        
        # Even/odd pattern
        if digit1 % 2 == digit2 % 2:  # Same parity
            score += 0.2
        else:
            score += 0.1
        
        # Digit sum
        digit_sum = digit1 + digit2
        if digit_sum <= 5:
            score += 0.3
        elif digit_sum >= 15:
            score += 0.2
        else:
            score += 0.1
        
        return score
    
    def get_smart_candidates(self, input_2d, day, context_score):
        """Dapatkan kandidat digit cerdas"""
        candidates = set()
        
        # Dari transition matrix
        if input_2d in self.transition_matrix:
            for next_2d in self.transition_matrix[input_2d]:
                candidates.update(next_2d)
        
        # Dari day patterns
        if day in self.day_patterns and input_2d in self.day_patterns[day]:
            for next_2d in self.day_patterns[day][input_2d]:
                candidates.update(next_2d)
        
        # Dari digit frequency
        if input_2d in self.digit_frequency:
            freq_digits = sorted(self.digit_frequency[input_2d].items(), 
                               key=lambda x: x[1], reverse=True)
            candidates.update([d[0] for d in freq_digits[:8]])
        
        # Add input digits
        candidates.update(input_2d)
        
        # Context-based additions
        if context_score > 1.5:
            # High context: add complementary digits
            for digit in input_2d:
                complement = str((10 - int(digit)) % 10)
                candidates.add(complement)
        
        return list(candidates)
    
    def ultra_strategy(self, input_2d, candidates, context_score):
        """Strategi ultra dengan optimization maksimal"""
        
        # Weighted selection based on frequency and context
        weighted_candidates = []
        
        for candidate in candidates:
            weight = 1.0
            
            # Frequency weight
            if input_2d in self.digit_frequency and candidate in self.digit_frequency[input_2d]:
                weight += self.digit_frequency[input_2d][candidate] * 0.1
            
            # Context weight
            weight += context_score * 0.2
            
            # Pattern weight
            if candidate in input_2d:
                weight += 0.3  # Boost input digits
            
            weighted_candidates.append((candidate, weight))
        
        # Sort by weight and select top 5
        weighted_candidates.sort(key=lambda x: x[1], reverse=True)
        
        bbfs = []
        for candidate, _ in weighted_candidates:
            if candidate not in bbfs:
                bbfs.append(candidate)
            if len(bbfs) >= 5:
                break
        
        # Fill with random if needed
        all_digits = [str(i) for i in range(10)]
        while len(bbfs) < 5:
            rand_digit = random.choice(all_digits)
            if rand_digit not in bbfs:
                bbfs.append(rand_digit)
        
        return bbfs[:5]
    
    def defensive_strategy(self, input_2d, candidates):
        """Strategi defensif untuk minimize losses"""
        # Prioritize high-frequency digits
        freq_candidates = []
        
        if input_2d in self.digit_frequency:
            freq_items = sorted(self.digit_frequency[input_2d].items(), 
                              key=lambda x: x[1], reverse=True)
            freq_candidates = [d[0] for d in freq_items[:3]]
        
        # Always include input digits
        bbfs = list(set(input_2d + freq_candidates))
        
        # Fill remaining
        remaining_candidates = [c for c in candidates if c not in bbfs]
        random.shuffle(remaining_candidates)
        
        for candidate in remaining_candidates:
            if len(bbfs) >= 5:
                break
            bbfs.append(candidate)
        
        # Fill with safe digits if needed
        safe_digits = ['1', '2', '3', '4', '5']
        for digit in safe_digits:
            if len(bbfs) >= 5:
                break
            if digit not in bbfs:
                bbfs.append(digit)
        
        return bbfs[:5]
    
    def aggressive_strategy(self, input_2d, candidates):
        """Strategi agresif untuk maximize wins"""
        # Use more diverse digit selection
        bbfs = []
        
        # Include input digits
        bbfs.extend(list(input_2d))
        
        # Add high-variance candidates
        remaining_candidates = [c for c in candidates if c not in bbfs]
        
        # Prioritize digits that appear in multiple contexts
        multi_context_digits = []
        for candidate in remaining_candidates:
            contexts = 0
            if input_2d in self.digit_frequency and candidate in self.digit_frequency[input_2d]:
                contexts += 1
            
            for day in self.day_patterns:
                if input_2d in self.day_patterns[day]:
                    for next_2d in self.day_patterns[day][input_2d]:
                        if candidate in next_2d:
                            contexts += 1
                            break
            
            if contexts > 1:
                multi_context_digits.append(candidate)
        
        # Add multi-context digits first
        for digit in multi_context_digits:
            if len(bbfs) >= 5:
                break
            if digit not in bbfs:
                bbfs.append(digit)
        
        # Fill remaining randomly
        all_digits = [str(i) for i in range(10)]
        random.shuffle(all_digits)
        for digit in all_digits:
            if len(bbfs) >= 5:
                break
            if digit not in bbfs:
                bbfs.append(digit)
        
        return bbfs[:5]
    
    def balanced_strategy(self, input_2d, candidates):
        """Strategi balanced"""
        # Mix of defensive and aggressive
        bbfs = []
        
        # Always include input digits (defensive)
        bbfs.extend(list(input_2d))
        
        # Add top frequency digit (defensive)
        if input_2d in self.digit_frequency:
            top_freq = max(self.digit_frequency[input_2d].items(), key=lambda x: x[1])
            if top_freq[0] not in bbfs:
                bbfs.append(top_freq[0])
        
        # Add diverse candidates (aggressive)
        remaining = [c for c in candidates if c not in bbfs]
        random.shuffle(remaining)
        
        for candidate in remaining[:2]:
            if len(bbfs) >= 5:
                break
            bbfs.append(candidate)
        
        # Fill remaining
        all_digits = [str(i) for i in range(10)]
        for digit in all_digits:
            if len(bbfs) >= 5:
                break
            if digit not in bbfs:
                bbfs.append(digit)
        
        return bbfs[:5]
    
    def test_strategy_rigorously(self, strategy_func, strategy_name, max_allowed_losses=5):
        """Test strategi dengan kriteria ketat"""
        print(f"Testing {strategy_name} dengan kriteria maksimal {max_allowed_losses} kalah beruntun...")
        
        results = []
        consecutive_losses = 0
        max_consecutive = 0
        total_wins = 0
        total_tests = min(1200, len(self.data) - 1)
        
        for i in range(total_tests):
            current = self.data[i]
            next_item = self.data[i + 1]
            
            # Generate BBFS
            bbfs = strategy_func(current['last_2d'], current['day'])
            
            # Test win condition
            bbfs_set = set(bbfs)
            next_2d_set = set(next_item['last_2d'])
            is_win = next_2d_set.issubset(bbfs_set)
            
            if is_win:
                consecutive_losses = 0
                total_wins += 1
            else:
                consecutive_losses += 1
                max_consecutive = max(max_consecutive, consecutive_losses)
            
            results.append({
                'test_no': i + 1,
                'date': current['date'].strftime('%Y-%m-%d'),
                'day': current['day'],
                'input_2d': current['last_2d'],
                'bbfs': bbfs,
                'next_2d': next_item['last_2d'],
                'win': is_win,
                'consecutive_losses': consecutive_losses
            })
            
            # Early termination if criteria not met
            if max_consecutive > max_allowed_losses and i > 200:
                print(f"  Early termination: Max consecutive losses {max_consecutive} > {max_allowed_losses}")
                break
        
        win_rate = (total_wins / len(results) * 100) if results else 0
        meets_criteria = max_consecutive <= max_allowed_losses
        
        performance = {
            'strategy_name': strategy_name,
            'total_tests': len(results),
            'wins': total_wins,
            'win_rate': round(win_rate, 2),
            'max_consecutive_losses': max_consecutive,
            'meets_criteria': meets_criteria,
            'results': results
        }
        
        print(f"  Total tests: {len(results)}")
        print(f"  Wins: {total_wins}")
        print(f"  Win rate: {win_rate:.2f}%")
        print(f"  Max consecutive losses: {max_consecutive}")
        print(f"  Meets criteria: {'✓ YA' if meets_criteria else '✗ TIDAK'}")
        
        return performance
    
    def intensive_search(self, max_iterations=100):
        """Pencarian intensif strategi optimal"""
        print(f"Memulai pencarian intensif dengan {max_iterations} iterasi...")
        print("Target: Maksimal 5 kalah beruntun dengan 1200+ test")
        
        best_performance = None
        strategies_tested = 0
        
        strategy_types = ["ultra", "defensive", "aggressive", "balanced"]
        
        for iteration in range(1, max_iterations + 1):
            print(f"\n--- Iterasi {iteration} ---")
            
            for strategy_type in strategy_types:
                strategies_tested += 1
                
                def current_strategy(input_2d, day):
                    return self.generate_smart_bbfs(input_2d, day, strategy_type)
                
                performance = self.test_strategy_rigorously(
                    current_strategy, 
                    f"{strategy_type.capitalize()}_Strategy_Iter{iteration}"
                )
                
                # Update best if better
                if (best_performance is None or 
                    performance['max_consecutive_losses'] < best_performance['max_consecutive_losses'] or
                    (performance['max_consecutive_losses'] == best_performance['max_consecutive_losses'] and
                     performance['win_rate'] > best_performance['win_rate'])):
                    
                    best_performance = performance
                    self.best_strategy = current_strategy
                
                # Success condition
                if performance['meets_criteria']:
                    print(f"\n🎉 STRATEGI OPTIMAL DITEMUKAN!")
                    print(f"Strategi: {performance['strategy_name']}")
                    print(f"Max consecutive losses: {performance['max_consecutive_losses']}")
                    print(f"Win rate: {performance['win_rate']}%")
                    print(f"Total strategies tested: {strategies_tested}")
                    return best_performance
            
            # Progress report
            if iteration % 10 == 0:
                current_best = best_performance['max_consecutive_losses'] if best_performance else "N/A"
                print(f"Progress: {strategies_tested} strategies tested, best max losses: {current_best}")
        
        print(f"\nSelesai pencarian intensif:")
        print(f"Total strategies tested: {strategies_tested}")
        if best_performance:
            if best_performance['meets_criteria']:
                print("✓ Strategi optimal ditemukan!")
            else:
                print(f"⚠️ Belum optimal. Best max losses: {best_performance['max_consecutive_losses']}")
        
        return best_performance
    
    def show_final_results(self, performance, sample_count=25):
        """Tampilkan hasil final dengan detail"""
        if not performance:
            print("Tidak ada hasil untuk ditampilkan")
            return
        
        print(f"\n{'='*60}")
        print(f"HASIL FINAL: {performance['strategy_name']}")
        print(f"{'='*60}")
        print(f"Total tests: {performance['total_tests']}")
        print(f"Total wins: {performance['wins']}")
        print(f"Win rate: {performance['win_rate']}%")
        print(f"Max consecutive losses: {performance['max_consecutive_losses']}")
        print(f"Memenuhi kriteria (≤5): {'✓ YA' if performance['meets_criteria'] else '✗ TIDAK'}")
        
        print(f"\nSample hasil ({sample_count} terakhir):")
        print("No  | Tanggal    | Hari    | Input | BBFS      | Next | Win | CL")
        print("-" * 70)
        
        sample_results = performance['results'][-sample_count:]
        for result in sample_results:
            status = "✓" if result['win'] else "✗"
            bbfs_str = "".join(result['bbfs'])
            print(f"{result['test_no']:3d} | {result['date']} | {result['day']:7s} | {result['input_2d']:5s} | {bbfs_str:9s} | {result['next_2d']:4s} | {status:3s} | {result['consecutive_losses']:2d}")

def main():
    print("=== ULTRA SMART BBFS SYSTEM ===")
    print("Sistem pencarian strategi BBFS dengan analisis ultra-mendalam")
    print("Kriteria sukses: Maksimal 5 kalah beruntun dengan 1200+ test real")
    
    # Initialize system
    system = UltraSmartBBFS()
    
    if not system.load_and_process_data():
        print("Gagal load data!")
        return None, None
    
    # Deep analysis
    system.deep_pattern_analysis()
    
    # Intensive search
    best_result = system.intensive_search(max_iterations=50)
    
    if best_result:
        # Show results
        system.show_final_results(best_result)
        
        # Demo predictions
        print(f"\n{'='*60}")
        print("DEMO PREDIKSI DENGAN STRATEGI TERBAIK")
        print(f"{'='*60}")
        
        demo_cases = ["3212", "4446", "6801", "2001", "5270"]
        for case in demo_cases:
            if len(case) >= 2:
                input_2d = case[-2:]
                day = "Senin"  # Demo day
                if system.best_strategy:
                    bbfs = system.best_strategy(input_2d, day)
                    bbfs_str = "".join(bbfs)
                    print(f"Input: {case} (2D: {input_2d}) → BBFS: {bbfs_str}")
        
        return system, best_result
    
    return None, None

if __name__ == "__main__":
    system, result = main()