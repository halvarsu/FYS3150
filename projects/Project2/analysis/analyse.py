import omega_analysis as interact
import argparse

def main(args):
    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})
    if args.stability_analysis:
        from stability_analysis import stability_analysis
        case = "non_interacting"
        method = args.method
        file_base = "build/{0}/{1}/".format(method, case)

        stability_analysis(file_base,args.figsize)

    if args.interacting_analysis:
        from omega_analysis import plot_interacting
        case = "interacting"
        method = args.method
        file_base = "build/{0}/{1}/".format(method, case)

        plot_interacting(args,file_base)

    if args.iterations_analysis:
        from stability_analysis import plot_iterations
        method = args.method
        file_dir = "build/{0}/".format(method)

        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1)
        plot_iterations(file_dir, ax)
        plt.savefig('')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stability_analysis',action="store_true",
            help="analyse stability")
    parser.add_argument('-i', '--interacting_analysis',action="store_true", 
            help="analyse interacting")
    parser.add_argument('-iter', '--iterations_analysis',action="store_true", 
            help="analyse iterations")
    parser.add_argument('-m', '--method',default='jacobi',
            choices =['arma','jacobi'])
    parser.add_argument('-N', '--dim',default=1000,
            type=int)
    parser.add_argument('-f', '--figsize',nargs=2,
            type=float, default=(6,4))
    args = parser.parse_args()
    main(args)
