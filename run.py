#!/usr/bin/python

""" A simple tool for running Python scripts by command line.  Use-cases will typically include scripts that do not require user input, require constant uptime, or scripts that may spend a long time computing something. """

import argparse
from cliheader import cliHeader
from subprocess import call, Popen
# from sys import stderr, path
from time import time
# from atexit import register

# def exit_hook

def run_script(script, args):
    """ Runs the script with any arguments passed to it.  Does basic error handling, and returns anything returned by the script back to our program. """
    try:
        process = Popen('python ' + script + ' ' + ' '.join(args), shell = True)
        process.wait()
        return process.returncode
    except Exception as e:
        print 'Exception when running script', e
        if process.returncode:
            return process.returncode
        else:
            return -1

def run_arg_parser():
    """ All of the configuration of the argument parser occurs here.  Returns the arg object."""
    header = cliHeader(title = 'pyTool', author = 'Ryan Holben', version = [0,0,1,'b'], whitespace = 1, bars = True)
    header.show_terse()

    parser = argparse.ArgumentParser(description='A small helper program used to launch python scripts.' )
    parser.add_argument('script', help = 'Name of the Python script to be launched.')
    parser.add_argument('args', help='All arguments listed after the script will be passed to it.', nargs=argparse.REMAINDER)
    parser.add_argument('-n', '--notify', help='Play a notification sound when the script terminates.', action = 'store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-k', '--keepalive', help='Keeps the script alive if it crashes by relaunching if it returns an error code.', action = 'store_true')
    group.add_argument('-kn', '--keepalive_n', help='Same as -k, but will only run the script up to a maximum of N times before giving up.', type=int, metavar='N')
    parser.add_argument('-r', '--repeat', help='Launches the script R times in succession.  When combined with -k or -kn, runs that end in errors do not count towards this number.  If set to -1, it will be relaunched forever, in which case the python instance running pyTool must be manually killed.  Do this with caution.', type=int, metavar='R')
    parser.add_argument('-s', '--stats', help='Displays basic statistics such as run time.  Also gives lap times when used with -r.', type=int)

    return parser.parse_args()

def main():
    args = run_arg_parser()

    if args.script:
        print 'Script:', args.script
    if args.args:
        print 'Args:', args.args
    # if args.arguments:
        # print 'Passing to script:', args
    if args.notify:
        print 'Audible notification enabled.'
    if args.keepalive:
        print 'The script will automatically relaunch if it returns an error code.'
    if args.keepalive_n:
        print 'The script will automatically relaunch up to', args.keepalive_n, 'times if it returns an error code.'
    if args.repeat:
        print 'The script will be run', args.repeat, 'times.'
        max_runs = args.repeat
    else:
        max_runs = 1

    times = []
    return_values = []
    successful_runs = 0
    failed_runs = 0
    keepalive_count = 0

    # register(exit_hook)

    while successful_runs < max_runs:
        prev_time = time()
        print '\n'+'-'*14 + args.script + ' run #' + str(successful_runs+1) + '/' + str(max_runs) + '-'*14
        return_val = run_script(args.script, args.args)
        print '\n'+'-'*50
        t = time() - prev_time

        if return_val == 0:
            print 'Success.  Returned:', return_val
            successful_runs += 1
            keepalive_count = 0
        else:
            print 'Error returned by script:', return_val
            failed_runs += 1
            if args.keepalive:
                print 'Relaunching...'
            elif args.keepalive_n:
                keepalive_count += 1
                print 'asdf'
                if keepalive_count <= args.keepalive_n:
                    print 'Relaunch attempt', str(keepalive_count) + '/' +str(args.keepalive_n) + '...'
                else:
                    print 'Failed too many times. Exiting.'
                    exit()
            else:
                print 'Exiting.'
                exit()

        return_values.append(return_val)
        times.append(t)
        print 'Elapsed: %0.3f s'%t


    print '\n All runs completed.'
    print 'Return values:', return_values
    print 'Successful runs:', successful_runs
    print 'Failed runs:', failed_runs
    print 'Average successful runtime: %0.03f s'%( sum(times)/len(times) )
    if args.notify:
        call('tput bel', shell=True)

main()
