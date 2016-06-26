#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

import random


class Bowllards(object):
    def __init__(self, success_rate):
        self.success_rate = success_rate
        self.quiet = False

    def is_success(self):
        return random.random() < self.success_rate

    def pocket_count(self, remain):
        """
        残り何球のうちいくつポケットできたか
        """
        for i in range(remain):
            if not self.is_success():
                return i

        return remain

    def make_frame(self):
        return {
            1: 0,
            2: 0,
            3: 0,
            'strike': False,
            'spare': False,
            'score': 0,
            'bare_score': 0,
            'additional_score': 0,
        }

    def play(self):
        frames = [self.make_frame() for _ in range(10)]

        for i in range(9):
            f = frames[i]
            remain_ball = 10
            pocket_count = self.pocket_count(remain_ball)
            f[1] = pocket_count

            # ストライク処理
            if i >= 1:
                if frames[i - 1]['spare'] or frames[i - 1]['strike']:
                    frames[i - 1]['additional_score'] += pocket_count
                    frames[i - 1]['score'] += pocket_count
            if i >= 2:
                if frames[i - 2]['strike'] and frames[i - 1]['strike']:
                    frames[i - 2]['additional_score'] += pocket_count
                    frames[i - 2]['score'] += pocket_count

            if pocket_count == 10:
                # ストライク
                f['strike'] = True
                f['score'] = f['bare_score'] = 10

            else:
                # ストライクでなかった
                remain_ball -= pocket_count
                pocket_count2 = self.pocket_count(remain_ball)

                if i >= 1:
                    if frames[i - 1]['strike']:
                        frames[i - 1]['additional_score'] += pocket_count
                        frames[i - 1]['score'] += pocket_count

                f[2] = pocket_count2
                f['score'] = f['bare_score'] = f[1] + f[2]
                if pocket_count2 == remain_ball:
                    f['spare'] = True

        # 10フレーム処理
        i = 9
        f = frames[i]
        remain_ball = 10
        pocket_count = self.pocket_count(remain_ball)

        # ストライク処理
        if frames[i - 1]['spare'] or frames[i - 1]['strike']:
            frames[i - 1]['additional_score'] += pocket_count
            frames[i - 1]['score'] += pocket_count
        if frames[i - 2]['strike'] and frames[i - 1]['strike']:
            frames[i - 2]['additional_score'] += pocket_count
            frames[i - 2]['score'] += pocket_count

        if pocket_count == 10:
            # 1投目ストライク
            f[1] = 10
            f['score'] = f['bare_score'] = 10

            pocket_count2 = self.pocket_count(10)
            # ストライク処理 (9フレーム目ストライクに加算)
            if frames[i - 1]['strike']:
                frames[i - 1]['additional_score'] += pocket_count2
                frames[i - 1]['score'] += pocket_count2
            # 2投目以降 ストライクでもそうでなくても処理は同じ
            f[2] = pocket_count2
            f['score'] += pocket_count2
            f['additional_score'] += pocket_count2

            pocket_count3 = self.pocket_count(10)
            f[3] = pocket_count3
            f['score'] += pocket_count3
            f['additional_score'] += pocket_count3

        else:
            remain_ball -= pocket_count
            pocket_count2 = self.pocket_count(remain_ball)

            if frames[i - 1]['strike']:
                frames[i - 1]['additional_score'] += pocket_count
                frames[i - 1]['score'] += pocket_count

            if pocket_count2 == remain_ball:
                f[2] = 10 - remain_ball
                f['score'] = f['bare_score'] = 10
                f['spare'] = True
                # 3投目ができる
                pocket_count3 = self.pocket_count(10)
                f[3] = pocket_count3
                f['score'] += pocket_count3
                f['additional_score'] += pocket_count3

            else:
                f[2] = pocket_count2
                f['score'] = f['bare_score'] = f[1] + f[2]

        # 集計と表示
        total_score = 0

        self.frame_log('Frame', 'Detail', 'B+A', 'S', 'Score', 'Total')
        for i, f in enumerate(frames):
            if i == 9:
                score_detail = '{},{},{}'.format(f[1], f[2], f[3])
            else:
                score_detail = '{},{}'.format(f[1], f[2])
            total_score += f['score']
            if f['strike']:
                s = 'X'
            elif f['spare']:
                s = '/'
            else:
                s = ' '
            self.frame_log(
                i + 1,
                score_detail,
                '{}+{}'.format(f['bare_score'], f['additional_score']),
                s,
                f['score'],
                total_score
            )
        return total_score

    def frame_log(self, *args):
        if not self.quiet:
            print('{:>5} {:<8} {:>6} {}{:>6}{:>6}'.format(*args))


def play_single():
    b = Bowllards(0.8)
    b.play()


def main():
    trial_count = 1000
    shoot_success_ratios = [0.5, 0.7, 0.8, 0.85, 0.9, 0.95, 0.99, 0.999, 0.9999]

    for s in shoot_success_ratios:
        scores = []
        for t in range(trial_count):
            b = Bowllards(s)
            b.quiet = True
            score = b.play()
            scores.append(float(score))
        # 算術平均
        avg = sum(scores) / len(scores)
        print('ratio:{:<6} avg:{:>7}'.format(s, avg))


if __name__ == '__main__':
    main()
